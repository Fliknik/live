# -*- coding: utf-8 -*-
from odoo import models, fields, api


class InheritPT(models.Model):
    _inherit = 'product.template'

    rmFirstName1 = fields.Char('Revmax First Name')
    rmFirstName2 = fields.Char('Revmax Second Name')

