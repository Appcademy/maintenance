# -*- coding: utf-8 -*-
from odoo import http

# class MaintenanceRepOrder(http.Controller):
#     @http.route('/maintenance_rep_order/maintenance_rep_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/maintenance_rep_order/maintenance_rep_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('maintenance_rep_order.listing', {
#             'root': '/maintenance_rep_order/maintenance_rep_order',
#             'objects': http.request.env['maintenance_rep_order.maintenance_rep_order'].search([]),
#         })

#     @http.route('/maintenance_rep_order/maintenance_rep_order/objects/<model("maintenance_rep_order.maintenance_rep_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('maintenance_rep_order.object', {
#             'object': obj
#         })