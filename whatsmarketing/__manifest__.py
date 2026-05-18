{
    'name': 'WhatsMarketing for Odoo',
    'version': '17.0.1.0.0',
    'category': 'Marketing',
    'summary': 'Send WhatsApp messages and templates from Odoo CRM using WhatsMarketing',
    'description': """
WhatsMarketing for Odoo
========================

Official WhatsApp Business API integration for Odoo CRM.
Send WhatsApp messages, share templates, and engage your leads
and contacts directly from Odoo using your WhatsMarketing account.

Features
--------
* Send WhatsApp text messages from Lead, Contact, and Customer forms
* Configure your WhatsMarketing API key in Settings
* Log every sent message as a chatter note on the record
* Send pre-approved WhatsApp templates with one click
* View message delivery status

Requirements
------------
* Active WhatsMarketing subscription (https://whatsmarketing.in)
* Valid WhatsApp Business API account onboarded with WhatsMarketing
    """,
    'author': 'Uttam Solution',
    'website': 'https://whatsmarketing.in',
    'support': 'support@whatsmarketing.in',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'contacts', 'crm'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/crm_lead_views.xml',
        'views/whatsmarketing_message_views.xml',
        'wizards/whatsmarketing_send_wizard_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
