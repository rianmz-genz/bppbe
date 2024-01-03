# -*- coding: utf-8 -*-
# from odoo import http


# class ManajemenTokoApi(http.Controller):
#     @http.route('/manajemen_toko_api/manajemen_toko_api/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/manajemen_toko_api/manajemen_toko_api/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('manajemen_toko_api.listing', {
#             'root': '/manajemen_toko_api/manajemen_toko_api',
#             'objects': http.request.env['manajemen_toko_api.manajemen_toko_api'].search([]),
#         })

#     @http.route('/manajemen_toko_api/manajemen_toko_api/objects/<model("manajemen_toko_api.manajemen_toko_api"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('manajemen_toko_api.object', {
#             'object': obj
#         })
