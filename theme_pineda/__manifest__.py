# -*- coding: utf-8 -*-
{
    'name': 'Pineda — Ferretería & Cerrajería',
    'description': 'Tema web industrial (rojo/amarillo/tinta) para ferretería y '
                   'cerrajería con entrega directa en obra. Recrea el design '
                   'system Pineda: hero con franja de peligro, categorías, '
                   'productos destacados, banner de entrega y catálogo eCommerce.',
    'summary': 'Tema industrial para ferretería y cerrajería (es-CO)',
    'category': 'Theme/Retail',
    'version': '18.0.1.0.0',
    'author': 'Andres Pineda',
    'license': 'LGPL-3',
    'depends': ['website', 'website_sale'],
    'data': [
        'views/snippets.xml',
        'views/snippets/s_pineda_products.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            'theme_pineda/static/src/scss/primary_variables.scss',
        ],
        'web.assets_frontend': [
            'https://unpkg.com/lucide@latest/dist/umd/lucide.min.js',
            'theme_pineda/static/src/scss/theme.scss',
            'theme_pineda/static/src/js/lucide_icons.js',
        ],
    },
    'images': [
        'static/description/cover.png',
    ],
}
