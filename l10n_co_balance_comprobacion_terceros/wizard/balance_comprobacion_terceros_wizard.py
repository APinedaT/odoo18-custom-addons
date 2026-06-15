from odoo import api, fields, models
from odoo.tools.misc import get_lang


class AccountBalanceComprobacionTercerosWizard(models.TransientModel):
    _name = "account.balance.comprobacion.terceros.wizard"
    _description = "Balance de Comprobacion por Terceros"

    company_id = fields.Many2one(
        comodel_name="res.company",
        string="Compania",
        required=True,
        readonly=True,
        default=lambda self: self.env.company,
    )
    journal_ids = fields.Many2many(
        comodel_name="account.journal",
        relation="bct_wizard_journal_rel",
        column1="wizard_id",
        column2="journal_id",
        string="Diarios",
        required=True,
        default=lambda self: self.env["account.journal"].search([
            ("company_id", "=", self.env.company.id)
        ]),
        domain="[(\"company_id\", \"=\", company_id)]",
    )
    date_from = fields.Date(string="Fecha inicial", required=True)
    date_to = fields.Date(string="Fecha final", required=True)
    target_move = fields.Selection(
        selection=[("posted", "Asientos publicados"), ("all", "Todos los asientos")],
        string="Movimientos objetivo",
        required=True,
        default="posted",
    )
    partner_ids = fields.Many2many(
        comodel_name="res.partner",
        relation="bct_wizard_partner_rel",
        column1="wizard_id",
        column2="partner_id",
        string="Terceros",
    )
    account_ids = fields.Many2many(
        comodel_name="account.account",
        relation="bct_wizard_account_rel",
        column1="wizard_id",
        column2="account_id",
        string="Cuentas",
        domain="[(\"company_ids\", \"in\", [company_id])]",
    )
    only_with_balance_or_movement = fields.Boolean(
        string="Solo con movimiento o saldo",
        default=True,
    )

    @api.onchange("company_id")
    def _onchange_company_id(self):
        if self.company_id:
            self.journal_ids = self.env["account.journal"].search(
                [("company_id", "=", self.company_id.id)]
            )

    def _build_contexts(self, form_data):
        return {
            "journal_ids": form_data.get("journal_ids") or False,
            "state": form_data.get("target_move") or "",
            "date_from": form_data.get("date_from") or False,
            "date_to": form_data.get("date_to") or False,
            "strict_range": True,
            "company_id": form_data.get("company_id") and form_data["company_id"][0] or False,
        }

    def action_print_pdf(self):
        self.ensure_one()
        data = {
            "ids": self.env.context.get("active_ids", []),
            "model": self.env.context.get("active_model", "ir.ui.menu"),
            "form": self.read(
                [
                    "company_id",
                    "journal_ids",
                    "date_from",
                    "date_to",
                    "target_move",
                    "partner_ids",
                    "account_ids",
                    "only_with_balance_or_movement",
                ]
            )[0],
        }
        data["form"]["used_context"] = dict(
            self._build_contexts(data["form"]),
            lang=get_lang(self.env).code,
        )
        return self.env.ref(
            "l10n_co_balance_comprobacion_terceros.action_report_balance_comprobacion_terceros"
        ).with_context(landscape=True).report_action(self, data=data)
