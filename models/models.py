# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class Broadcast(models.Model):
    _name = 'bt_broadcast.broadcast'
    _description = 'a model for broadcast'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Broadcast', required=True)
    description = fields.Text()
    is_notification = fields.Boolean(string='Notification Active?',help='Show notification web', )
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
        default='all_user', string="Type Receiver"
    )
    type_broadcast = fields.Selection(
        selection=[
            ("broadcast", "Broadcast"),
            ("notification", "Notification")],
        default='notification'
    )
    email = fields.Text(help='Email dapat diisi lebih dari satu, dan pisahkan dengan tanda koma (,)')
    specific_users = fields.Many2many('res.users', string='Users')
    department_ids = fields.Many2many('hr.department')   

    @api.onchange('type_broadcast')
    def get_type(self):
        for rec in self:
            if rec.type_broadcast == 'broadcast':
                self.is_notification = False
                
    # action broadcastsdb
    def action_broadcast(self):
        odoobot = self.env.ref('base.partner_root')
        emails = []
        partner_ids = []
        if self.type_recevier == 'email':
            emails = self.broadcast_by_emails()
        elif self.type_recevier == 'specific_user':
            emails = self.broadcast_by_users()
            for partner in self.specific_users:
                partner_ids.append(partner.partner_id.id)
        elif self.type_recevier == 'department':
            emails = self.broadcast_by_departments()
            employees = self.env['hr.employee'].search([('department_id','in',self.department_ids.ids)])
            for employee in employees:
                partner_ids.append(employee.user_id.partner_id.id)            
        elif self.type_recevier == 'all_user':
            emails = self.broadcast_by_all_users()
            self.broadcast_to_channel(odoobot)
            users = self.env['res.users'].search([])
            for user in users:
                partner_ids.append(user.partner_id.id)
        
        if len(emails) > 0:
            self.broadcast_to_email(odoobot, emails)
        if len(partner_ids) > 0:
            self.broadcast_to_inbox(odoobot, partner_ids)

    # do broadcast to direct message
    def broadcast_to_inbox(self, odoobot, partner_ids):
        channels = self.env["mail.channel"].sudo().search([])
        for channel in channels:
            if odoobot.id in channel.channel_last_seen_partner_ids.partner_id.ids and len(channel.channel_last_seen_partner_ids.ids) == 2:
                for partner in partner_ids:                    
                    if set(channel.channel_last_seen_partner_ids.partner_id.ids) == set([partner,odoobot.id]):
                        self.env["mail.channel"].sudo().search([('id','=',channel.id)]).message_post(
                            body = self.description,
                            subject = self.name,
                            author_id = odoobot.id,
                            message_type = 'comment',
                            subtype_xmlid = 'mail.mt_comment',
                        )             

    # do broadcast to general channel
    def broadcast_to_channel(self,odoobot):
        channel_general = self.env["mail.channel"].search([('name', '=', 'general')], limit=1)   
        if channel_general:     
            channel_general.message_post(
                body = self.description,
                subject = self.name,
                author_id = odoobot.id,
                message_type = 'comment',
                subtype_xmlid = 'mail.mt_comment',
            )

    # do send email
    def broadcast_to_email(self,odoobot, emails=[]):
        company = self.env.user.company_id
        mail = self.env['mail.mail'].sudo().create({
            'subject': self.name,
            'email_from': company.catchall_formatted or company.email_formatted,
            'author_id': odoobot.id,
            'email_to': ','.join([str(email) for email in emails]),
            'body_html': self.description,
        })
        mail.send() 

    # get email list from all users
    def broadcast_by_all_users(self):
        email_list = []
        users =  self.env['res.users'].search([])
        for user in users:
            email_list.append(user.email)
        return email_list

    # get email list from department
    def broadcast_by_departments(self):
        email_list = []
        departments =  self.env['hr.department'].search([('id','in', self.department_ids.ids)])
        for department in departments:
            email_list.append(department.member_ids.user_id.email)
        return email_list

    # get email list from specific users
    def broadcast_by_users(self):
        email_list = []
        for user in self.specific_users:
            email_list.append(user.email)
        return email_list

    # get email list from specific emails
    def broadcast_by_emails(self):
        email_list = []
        emails = self.email.split(',')
        for email in emails:
            email_list.append(email)
        return email_list

class Setting(models.Model):
    _name = "bt_broadcast.setting"
    _description = "Model for storing Personal settings"

    setting_key = fields.Char(string=_("Key Pengaturan"))
    setting_value = fields.Text(string=_("Isi Pengaturan"))
    setting_desc = fields.Text(string=_("Deskripsi Pengaturan"))
