# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosPaymentInh(models.Model):
    _inherit = 'pos.payment.method'

    receivable_account_id = fields.Many2one('account.account',
                                            string='Intermediary Account',
                                            required=True,
                                            domain=[],
                                            default=lambda
                                                self: self.env.company.account_default_pos_receivable_account_id,
                                            ondelete='restrict',
                                            help='Account used as counterpart of the income account in the accounting entry representing the pos sales.')
