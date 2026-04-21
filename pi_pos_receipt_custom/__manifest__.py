# -*- coding: utf-8 -*-
{
    'name': 'POS Pre Print',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': """Pre Print""",
    'description': """
          Allows you to print a pre-account at the retail point of sale similar to the restaurant type point of sale.
    """,
    'author': 'Andres Pineda',
    'depends': [
        'point_of_sale',
        'pos_restaurant'
    ],
    'data': [
        'views/res_config_settings_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            '/pi_pos_receipt_custom/static/src/xml/**',
            '/pi_pos_receipt_custom/static/src/js/**',
        ],
    },
    'installable': True,
    'application': False,
}
