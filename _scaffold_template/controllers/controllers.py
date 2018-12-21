# -*- coding: utf-8 -*-
from odoo import http

# class ExVa(http.Controller):
#     @http.route('/ex_va/ex_va/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ex_va/ex_va/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ex_va.listing', {
#             'root': '/ex_va/ex_va',
#             'objects': http.request.env['ex_va.ex_va'].search([]),
#         })

#     @http.route('/ex_va/ex_va/objects/<model("ex_va.ex_va"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ex_va.object', {
#             'object': obj
#         })