# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritRP(models.Model):
    _inherit = 'res.partner'

    bpn = fields.Char('BPN')

