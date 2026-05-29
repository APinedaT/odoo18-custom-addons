# -*- coding: utf-8 -*-
{
    'name': "POS No Pull-to-Refresh",
    'summary': "Previene pull-to-refresh en dispositivos móviles en el POS.",
    'category': 'Point of Sale',
    'version': '18.0.1.0.0',
    'license': 'LGPL-3',
    'depends': ['point_of_sale'],
    'data': [],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_no_pull_refresh/static/src/scss/pos_no_pull_refresh.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
