from odoo import api, fields, models
   from odoo.exceptions import UserError


   class CrmLead(models.Model):
       _inherit = 'crm.lead'

       whatsmarketing_message_count = fields.Integer(
           string='WhatsApp Messages',
           compute='_compute_whatsmarketing_message_count',
       )

       def _compute_whatsmarketing_message_count(self):
           for lead in self:
               lead.whatsmarketing_message_count = self.env['whatsmarketing.message'].search_count([
                   ('lead_id', '=', lead.id)
               ])

       def action_send_whatsmarketing_message(self):
           """Open the WhatsMarketing send wizard for this lead."""
           self.ensure_one()
           phone = self.mobile or self.phone
           if not phone:
               raise UserError("This lead has no phone or mobile number set.")
           return {
               'name': 'Send WhatsApp Message',
               'type': 'ir.actions.act_window',
               'res_model': 'whatsmarketing.send.wizard',
               'view_mode': 'form',
               'target': 'new',
               'context': {
                   'default_lead_id': self.id,
                   'default_partner_id': self.partner_id.id if self.partner_id else False,
                   'default_phone_number': phone,
               },
           }

       def action_view_whatsmarketing_messages(self):
           """View all WhatsApp messages sent for this lead."""
           self.ensure_one()
           return {
               'name': 'WhatsApp Messages',
               'type': 'ir.actions.act_window',
               'res_model': 'whatsmarketing.message',
               'view_mode': 'tree,form',
               'domain': [('lead_id', '=', self.id)],
           }
