# -*- coding: utf-8 -*-

from odoo import models, fields, api


class NewProduct(models.Model):
    _name = 'new.product'
    _description = 'manajemen_toko_api.manajemen_toko_api'

    name = fields.Char()
    price = fields.Integer()
    image = fields.Binary()
    user_id = fields.Many2one('res.users', string="User")

