from odoo import http, _, exceptions
from odoo.http import request
import json
from datetime import datetime

class AuthController(http.Controller):
    def __init__(self):
        super(AuthController, self).__init__()
        self.helper = request.env['service.helper']
        self.auth_service = request.env['service.auth']
        
    @http.route('/api/login', auth='public', methods=["POST"], csrf=False, cors="*")
    def login(self, **kw):
        kolom_dibutuhkan = ['email', 'password', 'db']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
        try:
            res = self.auth_service.prosesLogin(kw)
        except exceptions.AccessDenied as e:
            return self.helper.res_json([], False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil login')
    
    @http.route('/api/register', auth='public', methods=["POST"], csrf=False, cors="*", website=False)
    def register_user(self, **kw):
        kolom_dibutuhkan = ['email', 'password', 'name', 'image_1920', 'address', 'phone']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
        try:
            res = self.auth_service.processRegister(kw)
        except exceptions.AccessDenied as e:
            return self.helper.res_json([], False, f'{e}')
        return self.helper.res_json(res, True, 'Berhasil Mendaftar')

    @http.route('/api/upload-payment', auth='public', methods=["POST"], csrf=False, cors="*", website=False)
    def upload_payment(self, **kw):
        kolom_dibutuhkan = ['image', 'summary', 'user_id']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
        try:
            res = self.auth_service.uploadPayment(kw)
        except Exception as e:
            return self.helper.res_json([], False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil Mengupload')
    
    @http.route('/api/me', auth='public', methods=["POST"], csrf=False, cors="*", website=False)
    def me(self, **kw):
        kolom_dibutuhkan = ['uid']
        try:
            self.helper.validasi_kolom(kw, kolom_dibutuhkan)
        except exceptions.ValidationError as e:
            return self.helper.res_json([], False, f'Err {e}')
        try:
            res = self.auth_service.who_am_i(kw)
        except Exception as e:
            return self.helper.res_json([], False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil Mendapatkan data')

    @http.route('/api/self', auth='public', methods=["POST"], csrf=False, cors="*", website=False)
    def self_modify(self, **kw):
        try:
            res = self.auth_service.self_modify(kw)
        except Exception as e:
            return self.helper.res_json([], False, f'Err {e}')
        return self.helper.res_json(res, True, 'Berhasil Mengubah profil data')