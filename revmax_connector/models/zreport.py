from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools
from odoo.exceptions import ValidationError, UserError


class ZReport(models.Model):
    _name = 'z.report'

    date = fields.Date('Date')
    vat = fields.Char('VAT Number')
    bpnumber = fields.Char('BP Number')
    tax_office = fields.Char('Tax Office')
    z_number = fields.Char('Z Number')
    efd_serial = fields.Char('EFD Serial')
    registration_date = fields.Char('Registration Date')
    user = fields.Char('User')
    currency_id = fields.Char('Currency')
    dailytotal = fields.Char('Daily Total Amount')
    gross = fields.Char('Gross')
    corrections = fields.Char('Corrections')
    discounts = fields.Char('Discounts')
    surcharges = fields.Char('Surcharges')
    ticketsvoid = fields.Char('Tickets Void')
    ticketsvoidtotal = fields.Char('Tickets Void Total')
    ticketsfiscal = fields.Char('Tickets Fiscal')
    ticketsnonfiscal = fields.Char('Tickets Non Fiscal')
    vatrate = fields.Char('VAT Rate')
    netamount = fields.Char('Net Amount')
    taxamount = fields.Char('Tax Amount')

