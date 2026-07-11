from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    dian_alert_days_before_expiry = fields.Integer(
        string='Días antes de vencimiento de resolución',
        default=30,
    )
    dian_alert_number_percentage = fields.Integer(
        string='Porcentaje de uso del rango numérico',
        default=80,
    )
    dian_alert_draft_invoice_days = fields.Integer(
        string='Días de factura en borrador',
        default=2,
    )
    dian_alert_user_ids = fields.Many2many(
        'res.users',
        'company_dian_alert_user_rel',
        'company_id',
        'user_id',
        string='Destinatarios de alertas',
    )
