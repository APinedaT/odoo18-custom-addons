# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    @api.depends('pos_module_pos_restaurant', 'pos_config_id')
    def _compute_pos_module_pos_restaurant(self):
        for res_config in self:
            res_config.update({
                'pos_iface_printbill': True,
                'pos_iface_splitbill': True,
            })
