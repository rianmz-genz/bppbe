from odoo import api, models
from odoo import http, _, exceptions
from odoo.http import request
import base64

class AuthService(models.Model):
    _name = 'service.auth'
    _description = 'Auth Service'

    def get_uid(self, kw):
        uid = kw.get('uid')
        if uid:
            uid = int(kw.get('uid'))
        else:
            uid = False
        return uid

    @api.model
    def prosesLogin(self, kw):
        login = kw.get('email')
        password = kw.get('password')
        db = kw.get('db')
        User = request.env['res.users'].sudo()
        user = User.search([
            ('login', '=', login)
        ], limit=1)
        if not user:
            raise exceptions.AccessDenied(message="Pengguna tidak ditemukan")
        if not user.is_active:
            raise exceptions.AccessDenied(message="Pengguna belum aktif silahkan hubungi admin")
        try:
            http.request.session.authenticate(db, login, password)
        except Exception as e:
            raise exceptions.AccessDenied(message="Password tidak sesuai")
        return request.env['ir.http'].session_info()
    
    @api.model
    def processRegister(self, kw):
        name = kw.get('name')
        email = kw.get('email')
        password = kw.get('password')
        image_1920 = kw.get('image_1920')
        address = kw.get('address')
        phone = kw.get('phone')
        image_binary = base64.b64encode(image_1920.read()) if image_1920 else False
        # Buat data baru untuk user
        User = request.env['res.users'].sudo()
        exists = User.search([
            ('email', '=', email)
        ])
        if exists:
            raise exceptions.AccessDenied("Email sudah digunakan")
        user = User.create({
            'name': name,
            'login': email,
            'email': email,
            'password': password,
            'address': address,
            'image_1920': image_binary,
            'phone': phone,
        })
        image_base64 = image_binary.decode('utf-8') if image_binary else None
        return {
                    'user_id': user.id,
                    'name': name,
                    'login': email,
                    'email': email,
                    'password': password,
                    'image': image_base64,
                    'phone': phone,
                }

    @api.model
    def uploadPayment(self, kw):
        Payment = request.env['new.payment'].sudo()
        summary = kw.get('summary')
        user_id = kw.get('user_id')
        image = kw.get('image')
        image_binary = base64.b64encode(image.read()) if image else False
        payment = Payment.create({
            'image': image_binary,
            'summary': summary,
            'user_id': int(user_id),
        })
        if not payment:
            raise  exceptions.AccessDenied(message="Error create payment")
        image_base64 = image_binary.decode('utf-8') if image_binary else None
        return  {
            'id': payment.id,
            'user_id': user_id,
            'image': image_base64,
            'summary': summary
        }

    @api.model
    def who_am_i(self, kw):
        id = kw.get('uid')
        User = request.env['res.users'].sudo()
        try:
            user = User.search([
            ('id', '=', int(id))
            ], limit=1)
        except Exception as e:
            raise exceptions.AccessError(message=e)
        if not user:
            raise exceptions.AccessDenied(message="Pengguna tidak ditemukan")
        if not user.is_active:
            raise exceptions.AccessDenied(message="Pengguna belum aktif silahkan hubungi admin")
        image = False
        if user.image_1920:
            image = user.image_1920.decode('ascii')
        return {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone': user.phone,
            'address': user.address,
            'logo': image,
            'email': user.email,
        }

    @api.model
    def self_modify(self, kw):
        User = self.env['res.users'].sudo()

        # 1. Check for Invalid User ID
        user_id = int(kw.get("uid", 0))
        user = User.browse(user_id)
        if not user.exists():
            raise exceptions.AccessDenied(message="Pengguna tidak ditemukan")
        try:

            # Prepare the values to be updated
            if kw.get('password'):
                user.password = kw['password']
            if kw.get('name'):
                user.name = kw['name']
            if kw.get('email'):
                user.login = kw['email']
                user.email = kw['email']
            if kw.get('phone'):
                user.phone = kw['phone']
            if kw.get('address'):
                user.address = kw['address']
            if kw.get('image_1920'):
                user.image_1920 = base64.b64encode(kw['image_1920'].read())

        except Exception as e:
            raise  exceptions.AccessError(message=e)

        return {
            'id': user.id,
            'name': user.name,
        }
