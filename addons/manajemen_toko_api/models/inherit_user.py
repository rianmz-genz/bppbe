# -*- coding: utf-8 -*-

from odoo import models, fields, api


class InheritUser(models.Model):
    _inherit = 'res.users'

    is_active = fields.Boolean(default=False)
    address = fields.Text(string="Alamat")
    phone = fields.Text(string="No Handphone")
    
    def activate_user(self):
        self.is_active = True

