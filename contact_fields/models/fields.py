from odoo import api, fields, models


class ResInherit(models.Model):
    _inherit = "res.partner"

    itf_263 = fields.Selection([('register', 'Registered'), ('unregister', 'UnRegistered')], default='unregister')
    date_valid_from = fields.Date(string='Date Valid From', required=True)
    date_valid_to = fields.Date(string='Date Valid To', required=True)

    bp = fields.Selection([('register', 'Registered'), ('unregister', 'UnRegistered')], default='unregister')
    bp_number = fields.Char(string='BP No', required=True )


