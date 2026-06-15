# -*- coding: utf-8 -*-
from odoo import models


class Theme(models.AbstractModel):
    _inherit = 'theme.utils'

    def _theme_pineda_post_copy(self, mod):
        """Apply Pineda brand defaults when the theme is installed/applied.

        Selects a header with a search bar and a multi-column links footer
        (closest to the design), and locks the brand color palette + fonts so
        the website editor reflects them out of the box.
        """
        self.enable_view('website.template_header_search')
        self.enable_view('website.template_footer_links')

        self.env['web_editor.assets'].make_scss_customization(
            '/website/static/src/scss/options/user_values.scss',
            {
                'color-palettes-name': "'pineda'",
                'font': "'Barlow'",
                'headings-font': "'Saira'",
                'navbar-font': "'Saira'",
                'buttons-font': "'Saira'",
            },
        )
