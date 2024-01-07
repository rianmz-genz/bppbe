from odoo import api, models
from odoo import http, _, exceptions
from odoo.http import request
import json
class SaleService(models.Model):
    _name = 'service.sale'
    _description = 'Sale Service'
    def getUid(self, kw):
        uid = kw.get('uid')
        if uid:
            uid = int(kw.get('uid'))
        else:
            uid = 1
        return uid
    @api.model
    def get_all(self, kw):
        authorization_header = self.getUid(kw)
        Sale = http.request.env['new.sale'].sudo()
        sales = Sale.search([
            ('user_id', '=', int(authorization_header))
        ])
        if len(sales) == 0:
            raise exceptions.AccessError(message=f"Data Kosong {authorization_header}")
        sale_data = []
        for sale in sales:
            sale_data.append({
                'id': sale.id,
                'date': sale.date,
                'total': sale.total,
                'line_ids': [
                    {
                        'product_id': line.product_id.id, 
                        'name': line.product_id.name, 
                        'price': line.product_id.price, 
                        'qty': line.qty, 
                        'total': line.total,
                        'image': line.product_id.image.decode('ascii') if line.product_id.image else False
                    } for line in sale.line_ids
                ],
            })
        return sale_data
    
    @api.model
    def get_data_chart(self, kw):
        authorization_header = self.getUid(kw)
        Sale = http.request.env['new.sale'].sudo()

        # Group by date and sum total
        sales = Sale.search([
            ('user_id', '=', int(authorization_header))
        ])

        if not sales:
            raise exceptions.AccessError(message=f"Data Kosong {authorization_header}")

        sale_data = {}
        for sale in sales:
            date_key = sale.date
            total = sum(line.total for line in sale.line_ids)

            # Tambahkan ke objek yang memiliki tanggal yang sama
            if date_key in sale_data:
                sale_data[date_key]['total'] += total
            else:
                sale_data[date_key] = {'date': date_key, 'total': total}

        # Convert hasil ke dalam list array
        result_data = [{'date': item['date'], 'total': item['total']} for item in sale_data.values()]
        return result_data



    
    @api.model
    def get_by_id(self, id):
        sale = request.env['new.sale'].sudo().browse(id)
        if sale:
            sale_data = {
                'id': sale.id,
                'date': sale.date,
                'total': sale.total,
                'line_ids': [
                    {
                        'product_id': line.product_id.id, 
                        'name': line.product_id.name, 
                        'price': line.product_id.price, 
                        'qty': line.qty, 
                        'total': line.total,
                        'image': line.product_id.image.decode('ascii') if line.product_id.image else False
                    } for line in sale.line_ids
                ],
            }
            return sale_data
        raise exceptions.UserError(message="Penjualan tidak ditemukan")
    
    @api.model
    def create(self, kw):
        uid = kw.get('uid')
        if uid:
            uid = int(kw.get('uid'))
        else:
            uid = 1
        sale_data = json.loads(kw['data'])
        sale = request.env['new.sale'].sudo().create({
            'date': sale_data.get('date'),
            'user_id': uid,
        })
        if 'line_ids' in sale_data:
            for line in sale_data['line_ids']:
                product_id = line.get('product_id')
                qty = line.get('qty')
                if product_id and qty:
                    request.env['new.saleline'].sudo().create({
                        'product_id': product_id,
                        'qty': qty,
                        'sale_id': sale.id,
                    })
        return {
            'id': sale.id
        }