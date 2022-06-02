# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Broadcast(models.Model):
    _name = 'bt_broadcast.broadcast'
    _description = 'a model for broadcast'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Broadcast', required=True)
    description = fields.Text()
    is_notification = fields.Boolean(help='Show notification web', )
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

    def action_send_broadcast(self):
        if self.type_recevier == 'email':
            self.do_send_mail()
        elif self.type_recevier == 'department':
            self.do_send_department()
        elif self.type_recevier == 'specific_user':
            self.do_send_users()
        elif self.type_recevier == 'all_user':
            self.do_send_all_users()

    def do_send_mail(self):
        list_emails = self.email.split(',')
        for email in list_emails:
            template = self.env.ref('bt_broadcast.mail_template_starter', raise_if_not_found=False)
            template.email_to = email
            context = {
                'email_to': email,
                'subject': self.name,
                'body_html': self.description,
            }
            template.with_context(context).send_mail(self.id, force_send=True)

    def do_send_users(self):
        list_users = self.specific_users
        template = self.env.ref('bt_broadcast.mail_template_starter', raise_if_not_found=False)
        for user in list_users:
            template.subject = self.name
            template.email_to = user.email
            if self.description:
                template.body_html = self.description
            template.send_mail(self.id, force_send=True)

    def do_send_all_users(self):
        users = self.env['res.users'].search([])
        template = self.env.ref('bt_broadcast.mail_template_starter', raise_if_not_found=False)

        channel_general = self.env["mail.channel"].search([('name', '=', 'general')], limit=1)
        odoobot = self.env.ref('base.partner_root')
        # Sending message to channel general
        channel_general.message_post(
            body=self.description,
            subject=self.name,
            author_id=odoobot.id,
            message_type='comment',
            subtype_xmlid='mail.mt_comment',
        )
        for user in users:
            template.subject = self.name
            template.email_to = user.email
            if self.description:
                template.body_html = self.description
            template.send_mail(self.id, force_send=True)

    def do_send_department(self):
        departments = self.department_ids
        department = [department for department in departments]
        list_department = [department_one.member_ids for department_one in department]
        email_list = []
        template = self.env.ref('bt_broadcast.mail_template_starter', raise_if_not_found=False)
        for employee in list_department:
            for employee_one in employee:
                email_list.append(employee_one.user_id.email)
        for email in email_list:
            template.subject = self.name
            template.email_to = email
            if self.description:
                template.body_html = self.description
            template.send_mail(self.id, force_send=True)

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
