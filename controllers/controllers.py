# -*- coding: utf-8 -*-
# from odoo import http


# class BtBroadcast(http.Controller):
#     @http.route('/bt_broadcast/bt_broadcast/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bt_broadcast/bt_broadcast/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('bt_broadcast.listing', {
#             'root': '/bt_broadcast/bt_broadcast',
#             'objects': http.request.env['bt_broadcast.bt_broadcast'].search([]),
#         })

#     @http.route('/bt_broadcast/bt_broadcast/objects/<model("bt_broadcast.bt_broadcast"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bt_broadcast.object', {
#             'object': obj
#         })

import json

from odoo import http
from odoo.http import request


class BroadcastController(http.Controller):
    @http.route(['/broadcast'], type='http', auth="public", methods=['GET'], website=True, sitemap=False)
    def broadcast(self, broadcast=""):
        broadcast = request.env['bt_broadcast.broadcast'].search([('is_notification','=',True)], limit=1)

        return json.dumps({
            'name': broadcast.name,
            'description': broadcast.description,
            'type_notification': broadcast.type_notification,
            'is_notification': broadcast.is_notification,
        }, ensure_ascii=False)