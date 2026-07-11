import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _cron_check_draft_invoice_alerts(self):
        companies = self.env['res.company'].search([('ei_enable', '=', True)])

        for company in companies:
            days_threshold = company.dian_alert_draft_invoice_days
            if days_threshold is None:
                days_threshold = 2

            today = fields.Date.context_today(self)

            domain = [
                ('state', '=', 'draft'),
                ('move_type', 'in', ['out_invoice', 'out_refund']),
                ('company_id', '=', company.id),
            ]

            if days_threshold > 0:
                cutoff_date = today - relativedelta(days=days_threshold)
                domain.append(('create_date', '<=', fields.Date.to_string(cutoff_date)))

            draft_invoices = self.search(domain)
            if not draft_invoices:
                continue

            alert_users = company.dian_alert_user_ids
            if not alert_users:
                group = self.env.ref(
                    'l10n_co_edi_jorels.l10n_co_edi_jorels_group_manager',
                    raise_if_not_found=False,
                )
                if group:
                    alert_users = group.users

            if not alert_users:
                continue

            activity_type = self.env.ref(
                'pi_dian_alerts.mail_act_draft_invoice_reminder',
                raise_if_not_found=False,
            ) or self.env.ref('mail.mail_activity_data_todo')

            for invoice in draft_invoices:
                days_old = (today - invoice.create_date.date()).days
                for user in alert_users:
                    existing = self.env['mail.activity'].search([
                        ('res_model', '=', 'account.move'),
                        ('res_id', '=', invoice.id),
                        ('activity_type_id', '=', activity_type.id),
                        ('user_id', '=', user.id),
                    ], limit=1)
                    if not existing:
                        invoice.activity_schedule(
                            'pi_dian_alerts.mail_act_draft_invoice_reminder',
                            date_deadline=today,
                            summary=_("Factura borrador pendiente de validación"),
                            note=_(
                                "La factura %s lleva %d día(s) en estado borrador. "
                                "Por favor revise y valide.",
                                invoice.name or _('Nuevo'),
                                days_old,
                            ),
                            user_id=user.id,
                        )

            template = self.env.ref(
                'pi_dian_alerts.mail_template_draft_invoice_alert',
                raise_if_not_found=False,
            )
            if template:
                for user in alert_users:
                    template.with_context(
                        draft_invoices=draft_invoices,
                        alert_user=user,
                        days_threshold=days_threshold,
                    ).send_mail(
                        company.id,
                        force_send=False,
                        email_values={'email_to': user.email},
                    )
