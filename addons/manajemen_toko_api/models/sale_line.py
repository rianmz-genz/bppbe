from odoo import models, fields, api

class SaleLine(models.Model):
    _name = 'new.saleline'
    _description = 'Manajemen Toko API'

    product_id = fields.Many2one('new.product', string="Produk")
    qty = fields.Integer(string="Kuantitas")
    total = fields.Integer(string="Total", compute="_compute_total")
    sale_id = fields.Many2one('new.sale')
    @api.depends('product_id', 'qty')
    def _compute_total(self):
        for sale_line in self:
            if sale_line.product_id and sale_line.qty:
                sale_line.total = sale_line.product_id.price * sale_line.qty
            else:
                sale_line.total = 0
