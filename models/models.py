# -*- coding: utf-8 -*-

from odoo import models, fields


class Broadcast(models.Model):
    _name = 'bt_broadcast.broadcast'
    _description = 'a model for broadcast'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Broadcast', required=True)
    description = fields.Text()
    is_notification = fields.Boolean(help='Show notification web',)
    type_notification = fields.Selection(
        selection=[
                    ("info", "Info"),
                    ("warning", "Warning"),
                    ("danger", "Danger")],
        default='info'
    )
    type_recevier = fields.Selection(
        selection=[
                    ("email", "Email"),
                    ("specific_user", "Specific User"),
                    ("all_user", "All User"),
                    ("department", "Department")],
        default='all_user'
    )
    email = fields.Text()
    specific_users = fields.Many2many('res.users', string='Users')
    department_ids = fields.Many2many('hr.department')
