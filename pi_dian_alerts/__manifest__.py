{
    'name': 'Alertas DIAN - Resoluciones y Facturas Borrador',
    'version': '18.0.1.0.0',
    'author': 'Andres Pineda',
    'summary': 'Alertas de vencimiento de resoluciones DIAN y facturas borrador sin validar',
    'description': 'Alertas automáticas para resoluciones DIAN próximas a vencer '
                   '(por fecha o por rango numérico) y facturas de cliente en estado borrador.',
    'category': 'Invoicing & Payments',
    'depends': [
        'l10n_co_edi_jorels',
        'account',
        'mail',
    ],
    'data': [
        'data/mail_activity_type_data.xml',
        'data/mail_template_data.xml',
        'data/ir_cron_data.xml',
        'views/res_config_settings_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
