# -*- coding: utf-8 -*-
from odoo import http

class SetMultipaymentsLink(http.Controller):
    @http.route('/set/multipayments/link', auth='public')
    def index(self, **kw):
        res = http.request.env['multi.payments'].set_multi_payments_links()
        return 'done'
    @http.route('/set/jes/payments_links', auth='public')
    def index1(self, **kw):
        res = http.request.env['account.move.line'].set_jes_payments_links()
        return 'done'