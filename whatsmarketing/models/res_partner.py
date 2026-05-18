from odoo import api, fields, models
   from odoo.exceptions import UserError


   class ResPartner(models.Model):
       _inherit = 'res.partner'

       whatsmarketing_message_count = fields.Integer(
           string='WhatsApp Messages',
           compute='_compute_whatsmarketing_message_count',
       )

       def _compute_whatsmarketing_message_count(self):
           for partner in self:
               partner.whatsmarketing_message_count = self.env['whatsmarketing.message'].search_count([
                   ('partner_id', '=', partner.id)
               ])

       def action_send_whatsmarketing_message(self):
           """Open the WhatsMarketing send wizard for this contact."""
           self.ensure_one()
           if not self.phone and not self.mobile:
               raise UserError("This contact has no phone or mobile number set.")
           return {
               'name': 'Send WhatsApp Message',
               'type': 'ir.actions.act_window',
               'res_model': 'whatsmarketing.send.wizard',
               'view_mode': 'form',
               'target': 'new',
               'context': {
                   'default_partner_id': self.id,
                   'default_phone_number': self.mobile or self.phone,
               },
           }

       def action_view_whatsmarketing_messages(self):
           """View all WhatsApp messages sent to this contact."""
           self.ensure_one()
           return {
               'name': 'WhatsApp Messages',
               'type': 'ir.actions.act_window',
               'res_model': 'whatsmarketing.message',
               'view_mode': 'tree,form',
               'domain': [('partner_id', '=', self.id)],
           }
