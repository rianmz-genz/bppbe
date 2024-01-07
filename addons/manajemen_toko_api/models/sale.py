from odoo import models, fields, api

class NewSale(models.Model):
    _name = 'new.sale'
    _description = 'Manajemen Toko API'

    user_id = fields.Many2one('res.users', string="User")
    line_ids = fields.One2many('new.saleline', 'sale_id')
    date = fields.Char()
    total = fields.Integer(compute="_compute_total")

    @api.depends('line_ids.total')
    def _compute_total(self):
        for sale in self:
            total = sum(line.total for line in sale.line_ids)
            sale.total = total


