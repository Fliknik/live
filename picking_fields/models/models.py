# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    grv_no = fields.Char('GRV #')
    invoice_no = fields.Char('Invoice #')
    delivery_note = fields.Char('Delivery Note #')
