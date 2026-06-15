from datetime import timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ReportBalanceComprobacionTerceros(models.AbstractModel):
    _name = "report.l10n_co_balance_comprobacion_terceros.bct_report"
    _description = "Reporte Balance de Comprobacion por Terceros"

    def _get_move_states(self, target_move):
        if target_move == "posted":
            return ["posted"]
        return ["draft", "posted"]

    def _get_period_rows(self, form):
        used_context = form.get("used_context", {})
        query_get_data = self.env["account.move.line"].with_context(used_context)._query_get()
        where_clause = [query_get_data[1], '"account_move_line".partner_id IS NOT NULL']
        filter_params = []

        if form.get("partner_ids"):
            where_clause.append('"account_move_line".partner_id IN %s')
            filter_params.append(tuple(form["partner_ids"]))
        if form.get("account_ids"):
            where_clause.append('"account_move_line".account_id IN %s')
            filter_params.append(tuple(form["account_ids"]))

        params = [
            tuple(self._get_move_states(form.get("target_move"))),
            *query_get_data[2],
            *filter_params,
        ]

        query = """
            SELECT
                "account_move_line".account_id AS account_id,
                "account_move_line".partner_id AS partner_id,
                MAX("account_move_line".date) AS last_move_date,
                SUM("account_move_line".debit) AS debit,
                SUM("account_move_line".credit) AS credit
            FROM """ + query_get_data[0] + """
            JOIN account_move am ON am.id = "account_move_line".move_id
            WHERE am.state IN %s
              AND """ + " AND ".join(where_clause) + """
            GROUP BY
                "account_move_line".account_id,
                "account_move_line".partner_id
        """
        self.env.cr.execute(query, tuple(params))
        return self.env.cr.dictfetchall()

    def _get_previous_map(self, form):
        date_from = fields.Date.to_date(form.get("date_from"))
        if not date_from:
            return {}

        previous_context = dict(form.get("used_context", {}))
        previous_context["date_from"] = False
        previous_context["date_to"] = fields.Date.to_string(date_from - timedelta(days=1))
        previous_context["strict_range"] = False

        query_get_data = self.env["account.move.line"].with_context(previous_context)._query_get()
        where_clause = [query_get_data[1], '"account_move_line".partner_id IS NOT NULL']
        filter_params = []

        if form.get("partner_ids"):
            where_clause.append('"account_move_line".partner_id IN %s')
            filter_params.append(tuple(form["partner_ids"]))
        if form.get("account_ids"):
            where_clause.append('"account_move_line".account_id IN %s')
            filter_params.append(tuple(form["account_ids"]))

        params = [
            tuple(self._get_move_states(form.get("target_move"))),
            *query_get_data[2],
            *filter_params,
        ]

        query = """
            SELECT
                "account_move_line".account_id AS account_id,
                "account_move_line".partner_id AS partner_id,
                MAX("account_move_line".date) AS last_move_date,
                SUM("account_move_line".debit - "account_move_line".credit) AS previous_balance
            FROM """ + query_get_data[0] + """
            JOIN account_move am ON am.id = "account_move_line".move_id
            WHERE am.state IN %s
              AND """ + " AND ".join(where_clause) + """
            GROUP BY
                "account_move_line".account_id,
                "account_move_line".partner_id
        """
        self.env.cr.execute(query, tuple(params))

        previous_map = {}
        for row in self.env.cr.dictfetchall():
            key = (row["account_id"], row["partner_id"])
            previous_map[key] = {
                "previous_balance": row.get("previous_balance") or 0.0,
                "last_move_date": row.get("last_move_date"),
            }
        return previous_map

    def _prepare_lines(self, form):
        period_rows = self._get_period_rows(form)
        previous_map = self._get_previous_map(form)
        period_map = {
            (row["account_id"], row["partner_id"]): row
            for row in period_rows
        }

        keys = set(previous_map.keys()) | set(period_map.keys())
        currency = self.env.company.currency_id
        only_non_empty = form.get("only_with_balance_or_movement", True)
        account_map = {
            account.id: account
            for account in self.env["account.account"].browse(list({key[0] for key in keys}))
        }
        partner_map = {
            partner.id: partner
            for partner in self.env["res.partner"].browse(list({key[1] for key in keys if key[1]}))
        }

        grouped_lines = {}
        total_debit = 0.0
        total_credit = 0.0

        for key in sorted(keys, key=lambda item: (
            account_map.get(item[0]).code if account_map.get(item[0]) else "",
            partner_map.get(item[1]).name if partner_map.get(item[1]) else "",
            item[0],
            item[1],
        )):
            period_row = period_map.get(key, {})
            prev_row = previous_map.get(key, {})

            previous_balance = prev_row.get("previous_balance", 0.0)
            debit = period_row.get("debit", 0.0) or 0.0
            credit = period_row.get("credit", 0.0) or 0.0
            new_balance = previous_balance + debit - credit

            if only_non_empty and all(
                currency.is_zero(value)
                for value in [previous_balance, debit, credit, new_balance]
            ):
                continue

            total_debit += debit
            total_credit += credit

            account = account_map.get(key[0])
            partner = partner_map.get(key[1])
            account_code = account.code if account else ""
            account_name = account.name if account else ""
            partner_name = partner.name if partner else "-"
            grouped_lines.setdefault(key[0], {
                "account_id": key[0],
                "account_code": account_code,
                "account_name": account_name,
                "last_move_date": False,
                "previous_balance": 0.0,
                "debit": 0.0,
                "credit": 0.0,
                "new_balance": 0.0,
                "lines": [],
            })
            account_group = grouped_lines[key[0]]
            account_group["previous_balance"] += previous_balance
            account_group["debit"] += debit
            account_group["credit"] += credit
            account_group["new_balance"] += new_balance
            line_last_move_date = period_row.get("last_move_date") or prev_row.get("last_move_date")
            if line_last_move_date and (
                not account_group["last_move_date"] or line_last_move_date > account_group["last_move_date"]
            ):
                account_group["last_move_date"] = line_last_move_date

            account_group["lines"].append({
                "account_code": account_code,
                "description": partner_name,
                "last_move_date": period_row.get("last_move_date") or prev_row.get("last_move_date"),
                "previous_balance": previous_balance,
                "debit": debit,
                "credit": credit,
                "new_balance": new_balance,
            })

        lines = [
            grouped_lines[account_id]
            for account_id in sorted(
                grouped_lines,
                key=lambda account_id: (
                    grouped_lines[account_id]["account_code"],
                    grouped_lines[account_id]["account_name"],
                    account_id,
                ),
            )
        ]

        return lines, total_debit, total_credit

    @api.model
    def _get_report_values(self, docids, data=None):
        if not data or not data.get("form"):
            raise UserError(_("No se encontraron los parametros del reporte."))

        lines, total_debit, total_credit = self._prepare_lines(data["form"])
        return {
            "doc_ids": docids,
            "doc_model": "account.balance.comprobacion.terceros.wizard",
            "data": data,
            "lines": lines,
            "total_debit": total_debit,
            "total_credit": total_credit,
            "currency": self.env.company.currency_id,
        }
