from odoo import api, models
from odoo import http, _, exceptions
from odoo.http import request
import base64
class ProductService(models.Model):
    _name = 'service.product'
    _description = 'Product Service'
    def getUid(self, kw):
        uid = kw.get('uid')
        if uid:
            uid = int(kw.get('uid'))
        else:
            uid = 1
        return uid
    @api.model
    def getAll(self, kw):
        results = []
        Product = request.env['new.product'].sudo()
        uid = self.getUid(kw)
        try:
            products = Product.search([
                ('user_id', '=', uid)
            ])
        except Exception as e:
            raise exceptions.AccessError(message=e)
        
        if len(products) == 0:
            raise exceptions.UserError(message="Tidak Ada Product")
        
        for product in products:
            image = False
            if product.image:
                image = product.image.decode('ascii')
            results.append({
                'id': product.id,
                'name': product.name,
                'price': product.price,
                'image': image
            })
        return results
    
    @api.model
    def create(self, kw):
        Product = request.env['new.product'].sudo()
        uid = self.getUid(kw)
        try:
            image_binary = base64.b64encode(kw['image'].read()) if kw.get('image') else False

            # Buat produk baru dengan data yang diberikan
            new_product = Product.create({
                'name': kw['name'],
                'price': kw['price'],
                'user_id': uid,
                'image': image_binary
            })

        except Exception as e:
            raise exceptions.AccessError(message=e)

        # Konversi gambar (jika ada) ke format base64
        image_base64 = image_binary.decode('utf-8') if image_binary else None

        return {
            'id': new_product.id,
            'name': new_product.name,
            'price': new_product.price,
            'image': image_base64
        }
        
    @api.model
    def update(self, product_id, kw):
        Product = request.env['new.product'].sudo()
        product = Product.browse(product_id)
        
        try:
            # Perbarui data produk yang ada
            if kw['name']:
                product.write({'name': kw['name']})
            if kw['price']:
                product.write({'price': kw['price']})
            if kw['image']:
                image_binary = base64.b64encode(kw['image'].read())
                product.write({'image': image_binary})

        except Exception as e:
            raise exceptions.AccessError(message=e)
        
        image_base64 = image_binary.decode('utf-8') if image_binary else None

        return {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image': image_base64
        }
        
    @api.model
    def delete(self, product_id):
        Product = request.env['new.product'].sudo()
        product = Product.browse(product_id)
        
        try:
            # Hapus produk
            product.unlink()

        except Exception as e:
            raise exceptions.AccessError(message=e)

        return {
            'message': 'Produk berhasil dihapus.'
        }