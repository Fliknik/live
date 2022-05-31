from odoo import _, api, fields, models, modules, SUPERUSER_ID, tools


class CardDetail(models.Model):
    _name = 'card.detail'

    companyName = fields.Char('Company Name')
    addressLine1 = fields.Char('Address Line 1')
    addressLine2 = fields.Char('Address Line 2')
    addressLine3 = fields.Char('Address Line 3')
    vatNumber = fields.Char('VAT')
    registrationNumber = fields.Char('Registration Number')
    serialNumber = fields.Char('Serial Number')
    BPNumber = fields.Char('BP Number')

