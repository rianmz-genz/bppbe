from odoo import http, _, exceptions

from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception

class SaleApiController(http.Controller):
    def __init__(self):
        super(SaleApiController, self).__init__()
        self.helper = request.env['service.helper']
        self.sale_service = request.env['service.sale']
        
    @http.route('/api/sale/<int:sale_id>', auth='public', methods=['POST'], csrf=False, cors="*")
    def get_sale(self, sale_id, **kw):
        try:
            sale_data = self.sale_service.get_by_id(sale_id)
        except Exception as e:
            return self.helper.res_json({}, False, f'Err {e}')
        return self.helper.res_json(sale_data, True, 'Berhasil mendapatkan penjualan')
    
    @http.route('/api/sale/get_all', auth='public', methods=['POST'], csrf=False, cors="*")
    def get_all_sales(self, **kw):
        kolom_dibutuhkan = ['uid']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
        try:
            sale_data = self.sale_service.get_all(kw)
        except Exception as e:
            return self.helper.res_json({}, False, f'Err {e}')
        return self.helper.res_json(sale_data, True, 'Berhasil mendapatkan semua penjualan')

        
    @http.route('/api/sale/chart', auth='public', methods=['POST'], csrf=False, cors="*")
    def get_data_chart(self, **kw):
        kolom_dibutuhkan = ['uid']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
        try:
            sale_data = self.sale_service.get_data_chart(kw)
        except Exception as e:
            return self.helper.res_json({}, False, f'Err {e}')
        return self.helper.res_json(sale_data, True, 'Berhasil mendapatkan semua penjualan')

    @http.route('/api/sale/create', auth='public', methods=['POST'], csrf=False, cors="*")
    def create_sale(self, **kw):
        kolom_dibutuhkan = ['uid', 'data']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
        try:
            res = self.sale_service.create(kw)
        except Exception as e:
            return self.helper.res_json({}, False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil membuat penjualan')

