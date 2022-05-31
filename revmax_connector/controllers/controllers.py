# -*- coding: utf-8 -*-
# from odoo import http


# class RevmaxConnector(http.Controller):
#     @http.route('/revmax_connector/revmax_connector/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/revmax_connector/revmax_connector/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('revmax_connector.listing', {
#             'root': '/revmax_connector/revmax_connector',
#             'objects': http.request.env['revmax_connector.revmax_connector'].search([]),
#         })

#     @http.route('/revmax_connector/revmax_connector/objects/<model("revmax_connector.revmax_connector"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('revmax_connector.object', {
#             'object': obj
#         })
