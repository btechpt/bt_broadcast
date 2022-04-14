# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


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

    @api.onchange('type_recevier')
    def _onchange_type_recevier(self):
        if self.type_recevier == 'email':
            return {'value': {'specific_users': [], 'department_ids': []}}
        if self.type_recevier == 'specific_user':
            return {'value': {'email': '', 'department_ids': []}}
        if self.type_recevier == 'all_user':
            return {'value': {'email': '', 'specific_users': [], 'department_ids': []}}
        if self.type_recevier == 'department':
            return {'value': {'email': '', 'specific_users': []}}
