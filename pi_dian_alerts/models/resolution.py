import logging

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _

_logger = logging.getLogger(__name__)


class Resolution(models.Model):
    _inherit = 'l10n_co_edi_jorels.resolution'

    alert_number_usage_percent = fields.Float(
        string='Uso del rango (%)',
        compute='_compute_alert_fields',
    )
    alert_days_to_expiry = fields.Integer(
        string='Días para vencimiento',
        compute='_compute_alert_fields',
    )

    def _compute_alert_fields(self):
        today = fields.Date.context_today(self)
        for rec in self:
            total_range = rec.resolution_to - rec.resolution_from
            if total_range > 0 and rec.resolution_next_consecutive:
                try:
                    current = int(rec.resolution_next_consecutive)
                    used = current - rec.resolution_from
                    rec.alert_number_usage_percent = (used / total_range) * 100
                except (ValueError, TypeError):
                    rec.alert_number_usage_percent = 0.0
            else:
                rec.alert_number_usage_percent = 0.0

            if rec.resolution_date_to:
                rec.alert_days_to_expiry = (rec.resolution_date_to - today).days
            else:
                rec.alert_days_to_expiry = 9999

    @api.model
    def _cron_check_resolution_alerts(self):
        companies = self.env['res.company'].search([('ei_enable', '=', True)])

        for company in companies:
            resolutions = self.search([('company_id', '=', company.id)])
            if not resolutions:
                continue

            days_threshold = company.dian_alert_days_before_expiry or 30
            percent_threshold = company.dian_alert_number_percentage or 80
            today = fields.Date.context_today(self)
            alert_date_limit = today + relativedelta(days=days_threshold)

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

            expiring_date = self.env['l10n_co_edi_jorels.resolution']
            expiring_number = self.env['l10n_co_edi_jorels.resolution']

            for resolution in resolutions:
                if (resolution.resolution_date_to
                        and resolution.resolution_date_to <= alert_date_limit):
                    expiring_date |= resolution

                total_range = resolution.resolution_to - resolution.resolution_from
                if total_range > 0 and resolution.resolution_next_consecutive:
                    try:
                        current = int(resolution.resolution_next_consecutive)
                        used = current - resolution.resolution_from
                        usage_percent = (used / total_range) * 100
                        if usage_percent >= percent_threshold:
                            expiring_number |= resolution
                    except (ValueError, TypeError):
                        _logger.warning(
                            "Cannot parse resolution_next_consecutive '%s' for resolution %s",
                            resolution.resolution_next_consecutive,
                            resolution.name,
                        )

            all_expiring = expiring_date | expiring_number
            if all_expiring:
                self._send_resolution_alerts(
                    company, alert_users,
                    expiring_date, expiring_number,
                )

    def _send_resolution_alerts(self, company, users, expiring_date, expiring_number):
        AccountMove = self.env['account.move']
        activity_type = self.env.ref(
            'pi_dian_alerts.mail_act_resolution_expiring',
            raise_if_not_found=False,
        ) or self.env.ref('mail.mail_activity_data_todo')

        today = fields.Date.context_today(self)
        all_expiring = expiring_date | expiring_number

        for resolution in all_expiring:
            recent_move = AccountMove.search([
                ('resolution_id', '=', resolution.id),
                ('company_id', '=', resolution.company_id.id),
            ], order='create_date desc', limit=1)

            if not recent_move:
                continue

            notes = []
            if resolution in expiring_date:
                days_left = (resolution.resolution_date_to - today).days
                notes.append(_(
                    "La resolución '%s' vence el %s (%d días restantes).",
                    resolution.name,
                    resolution.resolution_date_to,
                    days_left,
                ))
            if resolution in expiring_number:
                try:
                    current = int(resolution.resolution_next_consecutive)
                    remaining = resolution.resolution_to - current
                    notes.append(_(
                        "La resolución '%s' tiene el rango numérico casi agotado: "
                        "actual %s, límite %s (%d números restantes).",
                        resolution.name,
                        resolution.resolution_next_consecutive,
                        resolution.resolution_to,
                        remaining,
                    ))
                except (ValueError, TypeError):
                    pass

            note_html = '<br/>'.join(notes)

            for user in users:
                existing = self.env['mail.activity'].search([
                    ('res_model', '=', 'account.move'),
                    ('res_id', '=', recent_move.id),
                    ('activity_type_id', '=', activity_type.id),
                    ('user_id', '=', user.id),
                ], limit=1)
                if not existing:
                    recent_move.activity_schedule(
                        'pi_dian_alerts.mail_act_resolution_expiring',
                        date_deadline=today,
                        summary=_("Alerta resolución DIAN: %s", resolution.name),
                        note=note_html,
                        user_id=user.id,
                    )

        template = self.env.ref(
            'pi_dian_alerts.mail_template_resolution_alert',
            raise_if_not_found=False,
        )
        if template and users:
            for user in users:
                template.with_context(
                    expiring_date=expiring_date,
                    expiring_number=expiring_number,
                    alert_user=user,
                ).send_mail(
                    company.id,
                    force_send=False,
                    email_values={'email_to': user.email},
                )
