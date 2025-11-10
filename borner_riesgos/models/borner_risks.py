# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from datetime import datetime, timedelta
import random

class Risk(models.Model):
    _name = 'borner.riesgo'

    date = fields.Date(string='Date', required=True)
    provider = fields.Many2one('res.partner', string='Provider', required=True)
    description = fields.Char(string='Description', required=True)
    amount = fields.Float(string='Amount', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
    ])
    risk = fields.Integer(string='Risk (%)')


    def set_risk(self):
        for record in self:
            numero_aleatorio = random.randint(1, 100)
            record.risk = numero_aleatorio