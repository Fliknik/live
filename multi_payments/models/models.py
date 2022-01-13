# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo import models, fields, api
from odoo.exceptions import Warning
from odoo.exceptions import ValidationError
import datetime
import logging


_logger = logging.getLogger(__name__)


class multi_payments(models.Model):
    _name = 'multi.payments'
    _description = 'Making Multi Payments '
    _rec_name= 's_no'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    name = fields.Char(string="name")
    s_no = fields.Char(string="Name")
    date = fields.Date(string="Date",track_visibility='onchange')
    journal_id = fields.Many2one('account.journal',string="Journal",track_visibility='onchange')
    amount = fields.Float(string="Amount",track_visibility='onchange')
    journal_item = fields.Many2one('account.move',string="Journal Entry",copy= False,track_visibility='onchange')
    company_id = fields.Many2one('res.company',string="Company",default=lambda self: self.env.company,track_visibility='onchange')
    payment_type =fields.Selection([
        ('outbound', 'Send Money'),
        ('inbound', 'Receive Money')
        ], string="Payment Type",default='outbound',track_visibility='onchange')
    partner_type =fields.Selection([
        ('customer', 'Customer'),
        ('supplier', 'Vendor'),
        ], string="Partner Type",track_visibility='onchange')

    voucher_type_o = fields.Selection([
        ('cpv', 'Cash Payment Voucher'),
        ('bpv', 'Bank Payment Voucher'),
        ],track_visibility='onchange')
    voucher_type_i = fields.Selection([
        ('crv', 'Cash Receipt Voucher'),
        ('brv', 'Bank Receipt Voucher'),
        ],track_visibility='onchange')

    state = fields.Selection([
        ('draft', 'Draft'),
        ('validate', 'Validate')
    ], string='Status', default='draft',track_visibility='onchange')

    def button_journal_ext(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'journal Item',
            'view_mode': 'tree,form',
            'res_model': 'account.move.line',
            'domain': [('move_id','=',self.journal_item.id)]
        }

    def set_multi_payments_links(self):
        records = self.search([('state','=','validate'),('id','>',490)], order='id', limit=100)
        _logger.info ("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        _logger.info (len(records))
        for payment in records:
            payment.button_draft()
            payment.button_verified()
            _logger.info ("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            _logger.info (payment.id)

    def button_draft(self):
        self.state = 'draft'
        self.journal_item.button_draft()
        self.journal_item.line_ids.unlink()
        # self.journal_item.unlink()

    def unlink(self): 
        for x in self: 
            if x.state in ["validate"]: 
                raise ValidationError('Cannot Delete Record') 
        rec = super(multi_payments,self).unlink()
        return rec

    @api.onchange('tree_link_id')
    def CalculateAmount(self):
        total = 0 
        for x in self.tree_link_id:
            total = total + x.amount

        self.amount = total

    @api.model
    def create(self, vals):
        if vals['payment_type'] == 'outbound':
            vals['s_no'] = self.env['ir.sequence'].next_by_code('outbound.payment.type')
        if vals['payment_type'] == 'inbound':
            vals['s_no'] = self.env['ir.sequence'].next_by_code('receive.payment.type')
        new_record = super(multi_payments, self).create(vals)

        return new_record

    def button_verified(self):
        self.state = 'validate'
        if not self.journal_item:
            self.create_journal_entry(self.journal_id,self.date,self.s_no,self.company_id.id)
        for lines in self.tree_link_id:
            if self.payment_type == 'inbound':
                credit_account = lines.partner_id_tree.property_account_receivable_id.id
                debit_account = self.journal_id.default_account_id.id
                create_debit = self.create_entry_lines(lines.partner_id_tree.id,self.date,lines.description,debit_account,lines.amount,0,self.journal_item.id, lines.description)
                create_credit = self.create_entry_lines(lines.partner_id_tree.id,self.date,lines.description,credit_account,0,lines.amount,self.journal_item.id, lines.description)
            if self.payment_type == 'outbound':
                credit_account = self.journal_id.default_account_id.id
                debit_account = lines.partner_id_tree.property_account_payable_id.id
                create_debit = self.create_entry_lines(lines.partner_id_tree.id,self.date,lines.description,debit_account,lines.amount,0,self.journal_item.id, lines.description)
                create_credit = self.create_entry_lines(lines.partner_id_tree.id,self.date,lines.description,credit_account,0,lines.amount,self.journal_item.id, lines.description)

        self.journal_item.action_post()
        for line in self.journal_item.line_ids:
            line.name = line.name +" "+line.payments_tree_label
        

    def create_journal_entry(self,journal,date,ref,company):
        if not self.journal_item:
            create_journal_entry = self.env['account.move'].create({
                'company_id': company,
                'journal_id': journal.id,
                'date': date,
                'move_type': 'entry',
                'ref':  ref,   
                })
            self.journal_item = create_journal_entry.id

    def create_entry_lines(self,partner,date,label,account,debit,credit,entry_id, description):
        self.env['account.move.line'].create({
            'account_id':account,
            'name': label,
            'debit':debit,
            'credit':credit,
            'move_id':entry_id,
            'partner_id':partner,
            'payments_tree_label':description,
            })

    # def set_all_record_company_ext(self):
    #     rec = self.env['multi.payments'].search([])
    #     company = self.env['res.company'].search([('id','=',1)])
    #     for x in rec:
    #         x.company_id = company.id



    tree_link_id = fields.One2many('multi.payments.tree', 'tree_link')




class multi_payments_tree(models.Model):
    _name = 'multi.payments.tree'
    _description = 'multi_payments.multi_payments.tree'
    _rec_name= 'name'


    name = fields.Char(string="name")
    partner_id_tree = fields.Many2one('res.partner',String="Partner" )
    description = fields.Char(string="Description")
    amount = fields.Float(string="Amount")


    @api.constrains('amount')
    def get_amount_payment(self):
        for rec in self:
            if rec.amount == 0:
                print('xxxxxxxxxxxxxxxxxxx')
                raise ValidationError(('"Amount should be greater than 0" '))

    tree_link = fields.Many2one('multi.payments')


class JouenalEntryLinePayExt(models.Model):
    _inherit = 'account.move.line'

    payments_tree_label = fields.Char("Payments Tree Label")


    def set_jes_payments_links(self):
        # records = self.search([('payments_tree_label','!=',False),('id','>',574)], order='id', limit=100)
        records = self.search([('payments_tree_label','!=',False)])
        _logger.info ("LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
        _logger.info (len(records))
        for line in records:
            _logger.info ("IIIIIIIIIIIIIIIIIIIIIIIIIIIII")
            _logger.info (line.id)
            line.name = line.name +" "+line.payments_tree_label

