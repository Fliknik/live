from odoo import api, models, fields, _
from datetime import datetime
from datetime import date


class DealPurchase(models.Model):
    _name = 'deal.purchase'
    _rec_name = 'vendor_id'

    ref = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: _('New'))
    vendor_id = fields.Many2one('res.partner', string="Vendor")
    date = fields.Date(string='Date')
    vendor_reference = fields.Char(string='Vendor Reference')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'confirmed')], default='draft', string="status")

    deal_lines_id = fields.One2many('deal.lines', 'deal_id')


    @api.model
    def create(self, vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('deal.purchase') or _('New')  # get seq. like : 'SO111'
        reference = str(vals['ref']).replace('DE', '')
        your_new_so_name = 'DE' + '/' + str(date.today().strftime("%y/%m/%d")) + '/' + reference
        vals.update({'ref': your_new_so_name})
        return super(DealPurchase, self).create(vals)

    def action_confirm(self):
        print("u click")
        self.state = 'confirm'

    def action_reset_draft(self):
        self.state = 'draft'


class DealLines(models.Model):
    _name = 'deal.lines'

    product_id = fields.Many2one('product.template' , string="Product")
    description = fields.Char('Description')
    qty = fields.Float('Quantity')
    received_qty = fields.Float('Quantity Received', readonly=True)
    unit_price = fields.Float('Unit Price')

    deal_id = fields.Many2one('deal.purchase')


