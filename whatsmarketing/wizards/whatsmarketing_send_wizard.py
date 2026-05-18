import requests
import logging
import json
from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WhatsMarketingSendWizard(models.TransientModel):
    _name = 'whatsmarketing.send.wizard'
    _description = 'WhatsMarketing Send Message Wizard'

    partner_id = fields.Many2one('res.partner', string='Contact')
    lead_id = fields.Many2one('crm.lead', string='Lead')
    phone_number = fields.Char(
        string='Phone Number (with country code)',
        required=True,
        help='Phone number with country code, only numeric. Example: 919876543210',
    )
    message_type = fields.Selection([
        ('text', 'Text Message'),
        ('template', 'Template Message'),
    ], string='Message Type', default='text', required=True)
    message_body = fields.Text(string='Message')
    template_id = fields.Char(
        string='Template ID',
        help='Numeric template ID from your WhatsMarketing dashboard',
    )

    @api.onchange('phone_number')
    def _onchange_phone_number(self):
        """Strip non-numeric characters from phone number."""
        if self.phone_number:
            cleaned = ''.join(filter(str.isdigit, self.phone_number))
            if cleaned != self.phone_number:
                self.phone_number = cleaned

    def action_send(self):
        """Send the WhatsApp message via WhatsMarketing API."""
        self.ensure_one()

        ICP = self.env['ir.config_parameter'].sudo()
        api_key = ICP.get_param('whatsmarketing.api_key')
        phone_number_id = ICP.get_param('whatsmarketing.phone_number_id')
        base_url = ICP.get_param('whatsmarketing.base_url', 'https://app.whatsmarketing.in/api/v1')

        if not api_key:
            raise UserError(_(
                "WhatsMarketing API key is not configured. "
                "Go to Settings -> General Settings -> WhatsMarketing to set it up."
            ))
        if not phone_number_id:
            raise UserError(_(
                "WhatsMarketing Phone Number ID is not configured. "
                "Go to Settings -> General Settings -> WhatsMarketing to set it up."
            ))

        if not self.phone_number:
            raise UserError(_("Please enter a phone number with country code."))

        log_vals = {
            'partner_id': self.partner_id.id if self.partner_id else False,
            'lead_id': self.lead_id.id if self.lead_id else False,
            'phone_number': self.phone_number,
            'message_body': self.message_body or '',
            'message_type': self.message_type,
            'status': 'pending',
        }
        log = self.env['whatsmarketing.message'].create(log_vals)

        try:
            if self.message_type == 'text':
                if not self.message_body:
                    raise UserError(_("Please enter a message to send."))
                url = base_url.rstrip('/') + '/whatsapp/send'
                payload = {
                    'apiToken': api_key,
                    'phone_number_id': phone_number_id,
                    'message': self.message_body,
                    'phone_number': self.phone_number,
                }
            else:
                if not self.template_id:
                    raise UserError(_("Please enter a template ID to send."))
                url = base_url.rstrip('/') + '/whatsapp/send/template'
                payload = {
                    'apiToken': api_key,
                    'phone_number_id': phone_number_id,
                    'template_id': self.template_id,
                    'phone_number': self.phone_number,
                }

            response = requests.post(url, data=payload, timeout=30)
            response_text = response.text
            _logger.info("WhatsMarketing API response: %s", response_text)
            log.api_response = response_text

            try:
                response_json = response.json()
            except (ValueError, json.JSONDecodeError):
                response_json = {}

            if response.status_code == 200 and str(response_json.get('status', '')) == '1':
                log.status = 'sent'
                log.wa_message_id = response_json.get('wa_message_id', '')

                note_body = _("WhatsApp message sent to %s: %s") % (
                    self.phone_number,
                    self.message_body or ("Template ID " + str(self.template_id)),
                )
                if self.partner_id:
                    self.partner_id.message_post(body=note_body, subject="WhatsApp Sent")
                if self.lead_id:
                    self.lead_id.message_post(body=note_body, subject="WhatsApp Sent")

                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': _('Success'),
                        'message': _('WhatsApp message sent successfully.'),
                        'type': 'success',
                        'sticky': False,
                    }
                }
            else:
                error_msg = response_json.get('message', 'Unknown error from WhatsMarketing API')
                log.status = 'failed'
                raise UserError(_("Failed to send WhatsApp message: %s") % error_msg)

        except requests.exceptions.Timeout:
            log.status = 'failed'
            log.api_response = "Request timed out"
            raise UserError(_("Request to WhatsMarketing API timed out. Please try again."))
        except requests.exceptions.RequestException as e:
            log.status = 'failed'
            log.api_response = str(e)
            raise UserError(_("Network error contacting WhatsMarketing API: %s") % str(e))
