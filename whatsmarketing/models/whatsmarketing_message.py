from odoo import api, fields, models


class WhatsMarketingMessage(models.Model):
    _name = 'whatsmarketing.message'
    _description = 'WhatsMarketing Sent Message Log'
    _order = 'create_date desc'

    partner_id = fields.Many2one('res.partner', string='Contact', ondelete='set null')
    lead_id = fields.Many2one('crm.lead', string='Lead/Opportunity', ondelete='set null')
    phone_number = fields.Char(string='Phone Number', required=True)
    message_body = fields.Text(string='Message')
    message_type = fields.Selection([
        ('text', 'Text Message'),
        ('template', 'Template Message'),
    ], string='Message Type', default='text', required=True)
    status = fields.Selection([
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ], string='Status', default='pending')
    wa_message_id = fields.Char(string='WhatsApp Message ID')
    api_response = fields.Text(string='API Response')
    user_id = fields.Many2one('res.users', string='Sent By', default=lambda self: self.env.user)
