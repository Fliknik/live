from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime


class DealPurchase(models.Model):
    _name = 'deal.purchase'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref'

    ref = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'),
                      tracking=True)
    vendor_id = fields.Many2one('res.partner', string="Vendor", tracking=True)
    date = fields.Date(string='Date', tracking=True, required=True)
    vendor_reference = fields.Char(string='Vendor Reference', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'confirmed'), ('cancel', 'Cancelled')], default='draft',
                             string="status", tracking=True)

    deal_lines_id = fields.One2many('deal.lines', 'deal_id')

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('deal.purchase') or _('New')  # get seq. like : 'SO111'
        reference = str(vals['ref']).replace('DE', '')
        d1 = datetime.strptime(str(vals['date']), "%Y-%m-%d").date()
        your_new_so_name = f'DE/{d1.year}/{d1.month}/{reference}'
        vals.update({'ref': your_new_so_name})
        return super(DealPurchase, self).create(vals)

    def write(self, vals):
        if 'date' in vals:
            print(self.ref)
            reference = self.ref.split('/')
            print(reference[3])
            d1 = datetime.strptime(str(vals['date']), "%Y-%m-%d")
            your_new_so_name = f'DE/{d1.year}/{d1.month}/{reference[3]}'
            vals.update({'ref': your_new_so_name})
        return super(DealPurchase, self).write(vals)

    def action_confirm(self):
        self.state = 'confirm'

    def action_reset_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'

    def unlink(self):
        for s in self:
            if s.state not in ('draft', 'cancel'):
                raise UserError(
                    'You cannot delete which is not in draft or cancelled state')
        return super(DealPurchase, self).unlink()


class DealLines(models.Model):
    _name = 'deal.lines'

    product_id = fields.Many2one('product.template', string="Product")
    description = fields.Char('Description')
    qty = fields.Float('Quantity')
    received_qty = fields.Float('Quantity Received', compute="_compute_received_quantity")
    unit_price = fields.Float('Unit Price')
    sub_total = fields.Float('SubTotal', readonly=True)

    deal_id = fields.Many2one('deal.purchase')

    @api.onchange('qty', 'unit_price', 'sub_total')
    def _function_subtotal(self):
        for rec in self:
            rec.sub_total = rec.qty * rec.unit_price

    @api.depends('product_id')
    def _compute_received_quantity(self):
        for rec in self:
            record = self.env['stock.picking'].search([('deal_id', '=', rec.deal_id.ref)])
            r = 0
            for l in record.move_ids_without_package:
                r = r + l.qty_kg
            rec.received_qty = r


class PurchaseOrderDeal(models.Model):
    _inherit = "purchase.order"

    deal_id = fields.Many2one('deal.purchase', string='Deals')
    # qty_kg = fields.Float(string='Qty Kgs')


    def button_confirm(self):
        res = super(PurchaseOrderDeal, self).button_confirm()
        for rec in self:
            for pick_rec in rec.picking_ids:
                pick_rec.write({
                    'deal_id': rec.deal_id.ref
                })
            for r in rec.order_line:
                for i in pick_rec.move_ids_without_package:
                    i.write({
                        'qty_kg': r.qty_kg
                    })
        return res


class StockPickingField(models.Model):
    _inherit = "stock.picking"

    deal_id = fields.Char(string='Deals', readonly=True)


class PurchaseOrderLineQty(models.Model):
    _inherit = "purchase.order.line"

    qty_kg = fields.Float(string='Qty in Kgs')


class StockMoveLineQty(models.Model):
    _inherit = "stock.move"

    qty_kg = fields.Float(string='Qty in Kgs')




