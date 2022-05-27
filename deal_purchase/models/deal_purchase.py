from odoo import api, models, fields, _
from datetime import date
from odoo.exceptions import UserError, ValidationError
from datetime import datetime

class DealPurchase(models.Model):
    _name = 'deal.purchase'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ref'

    ref = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'),
                      tracking=True)
    vendor_id = fields.Many2one('res.partner', string="Vendor", tracking=True)
    date = fields.Date(string='Date', tracking=True)
    vendor_reference = fields.Char(string='Vendor Reference', tracking=True)
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'confirmed'), ('cancel', 'Cancelled')], default='draft',
                             string="status", tracking=True)

    deal_lines_id = fields.One2many('deal.lines', 'deal_id')

    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('deal.purchase') or _('New')  # get seq. like : 'SO111'
        reference = str(vals['ref']).replace('DE', '')
        if vals['date']:
            print(type(vals['date']))
            d1 = datetime.strptime(str(vals['date']), "%Y-%m-%d").date()

            # my_date = datetime.strptime(vals['date'], "%Y-%m-%d")
            # my_date = vals['date'].year
            # print(type(vals['date']))
            # print(my_date.month)

            your_new_so_name = f'DE/{d1.year}/{d1.month}/{reference}'
            vals.update({'ref': your_new_so_name})
        return super(DealPurchase, self).create(vals)

    def write(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('deal.purchase') or _('New')  # get seq. like : 'SO111'
        reference = str(vals['ref']).replace('DE', '')
        if vals['date']:
            print(type(vals['date']))

            d1 = datetime.strptime(vals['date'], "%Y-%m-%d").date()
            your_new_so_name = f'DE/{d1.year}/{d1.month}/{reference}'
            vals.update({'ref': your_new_so_name})
        return super(DealPurchase, self).write(vals)

    def action_confirm(self):
        print("u click")
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
    received_qty = fields.Float('Quantity Received' , compute = "_compute_received_quantity")
    unit_price = fields.Float('Unit Price')
    sub_total = fields.Float('SubTotal', readonly=True)

    deal_id = fields.Many2one('deal.purchase')



    @api.onchange('qty', 'unit_price', 'sub_total')
    def _function_subtotal(self):
        for rec in self:
            rec.sub_total = rec.qty * rec.unit_price

    @api.depends('received_qty')
    def _compute_received_quantity(self):
        for rec in self:
            result = self.env['deal.purchase'].browse(self.env.context.get('active_ids'))
            print(result)
            record = self.env['stock.picking'].search([('deal_id', '=', rec.deal_id.id)])
            print(record)
            r = 0
            for l in record.move_ids_without_package:
                if l.product_id.id == rec.product_id.id:
                    r = r+l.quantity_done
            rec.received_qty = r


class SaleOrder(models.Model):
    _inherit = "purchase.order"

    deal_id = fields.Many2one('deal.purchase', string='Deals')


class StockPickingField(models.Model):
    _inherit = "stock.picking"

    deal_id = fields.Many2one('deal.purchase', string='Deals')
