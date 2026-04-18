# -*- coding: utf-8 -*-
{
    'name': 'Product price Display on POS',
    'version': '18.0.1.0.0',
    'summary': 'Display the correct tax-inclusive product price on POS product cards',
    'category': 'Point Of Sale',
    'depends': ['point_of_sale'],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_price/static/src/app/display_price.css',
            'pos_price/static/src/app/ProductCardFixed.xml',
        ],
    },
    "images": [
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
