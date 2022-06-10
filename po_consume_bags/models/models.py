# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrderInherited(models.Model):
    _inherit = 'purchase.order'

    def consume_bags(self):
        record = self.env['stock.picking.type'].search([('bag_consumption','=',True)])
        print('---------------------------------------------')
        for rec in record:
            print(rec.name)
        return {
            'name': _('Transfers'),
            # 'domain': [('picking_type_id', 'in', record.id)],
            # 'domain': [('picking_type_id.bag_consumption', '=', True)],
            'context': {'default_btn_record': True},
            'view_type': 'form',
            'res_model': 'stock.picking',
            'view_id': False,
            'view_mode': 'form',
            'type': 'ir.actions.act_window',
        }

    cb_counter = fields.Integer(string='PO', compute='get_consumption_counter')

    def get_consumption_counter(self):
        for rec in self:
            count = self.env['stock.picking'].search_count([('btn_record', '=', True)])
            rec.cb_counter = count

    def get_consumptions(self):
        # records = self.env['stock.picking'].search([()])
        return {
            'name': _('Transfers'),
            'domain': [('btn_record', '=', True)],
            'context': {'default_btn_record': True},
            'view_type': 'form',
            'res_model': 'stock.picking',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }


class StockPickingTypes(models.Model):
    _inherit = 'stock.picking.type'
    bag_consumption = fields.Boolean('Bag Consumption')


class StockPickingInherited(models.Model):
    _inherit = 'stock.picking'

    # purchase_id = fields.Many2one('purchase.order')
    btn_record = fields.Boolean(default=False)
