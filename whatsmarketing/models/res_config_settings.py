from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    whatsmarketing_api_key = fields.Char(
        string='WhatsMarketing API Key',
        config_parameter='whatsmarketing.api_key',
        help='Your API key from your WhatsMarketing developer console. '
             'Get it from app.whatsmarketing.in/api/developer/console',
    )
    whatsmarketing_phone_number_id = fields.Char(
        string='WhatsApp Phone Number ID',
        config_parameter='whatsmarketing.phone_number_id',
        help='Your WhatsApp Business phone number ID from WhatsMarketing',
    )
    whatsmarketing_base_url = fields.Char(
        string='API Base URL',
        config_parameter='whatsmarketing.base_url',
        default='https://app.whatsmarketing.in/api/v1',
        help='Base URL of WhatsMarketing API. Do not change unless instructed by support.',
    )
