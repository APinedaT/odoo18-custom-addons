from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    dian_alert_days_before_expiry = fields.Integer(
        related='company_id.dian_alert_days_before_expiry',
        readonly=False,
    )
    dian_alert_number_percentage = fields.Integer(
        related='company_id.dian_alert_number_percentage',
        readonly=False,
    )
    dian_alert_draft_invoice_days = fields.Integer(
        related='company_id.dian_alert_draft_invoice_days',
        readonly=False,
    )
    dian_alert_user_ids = fields.Many2many(
        related='company_id.dian_alert_user_ids',
        readonly=False,
    )
