from odoo import http, _, exceptions
from odoo.http import request
import json
from datetime import datetime

import logging
logg = logging.getLogger(__name__)

class ProductController(http.Controller):
    def __init__(self):
        super(ProductController, self).__init__()
        self.helper = request.env['service.helper']
        self.product_service = request.env['service.product']
        
    @http.route('/api/products/all', auth='public', methods=["POST"], csrf=False, cors="*")
    def getAll(self, **kw):
        kolom_dibutuhkan = ['uid']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
       
        try:
            res = self.product_service.getAll(kw)
        except Exception as e:
            return self.helper.res_json([], False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil mendapatkan semua produk')
    
    @http.route('/api/products/create', auth='public', methods=["POST"], csrf=False, cors="*")
    def buat(self, **kw):
        logg.info(f"kwwwww {kw}")
        kolom_dibutuhkan = ['name', 'price', 'image', 'uid']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
        try:
            res = self.product_service.create(kw)
        except Exception as e:
            return self.helper.res_json([], False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil edit product')
    
    @http.route('/api/products/update/<int:id>', auth='public', methods=["POST"], csrf=False, cors="*")
    def update(self, id,**kw):
        try:
            res = self.product_service.update(id, kw)
        except Exception as e:
            return self.helper.res_json([], False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil mendapatkan semua produk')
    
    @http.route('/api/products/delete/<int:id>', auth='public', methods=["POST"], csrf=False, cors="*")
    def create(self, id,**kw):
        if not id:
            return self.helper.res_json([], False, f'Err id required')
        try:
            res = self.product_service.delete(id)
        except Exception as e:
            return self.helper.res_json([], False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil hapus product')