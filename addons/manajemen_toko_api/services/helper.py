from odoo import api, models, exceptions
from base64 import b64encode, b64decode
from odoo.http import request
import json

class AuthService(models.Model):
    _name = 'service.helper'
    _description = 'Helper'

    @api.model
    def validasi_kolom(self, kw, required_fields):
        for field_name in required_fields:
            if field_name not in kw or not kw[field_name]:
                raise exceptions.ValidationError(message=f'`{field_name}` is required.')

    @api.model
    def encrypt(self, text):
        encoded_bytes = b64encode(text.encode('utf-8'))
        encoded_string = encoded_bytes.decode('utf-8')
        return encoded_string
    
    @api.model
    def decrypt(self, encoded_string):
        decoded_bytes = b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    
    @api.model
    def res_json(self, result, status, message):
        return request.make_response(
                json.dumps(
                    {
                        'message': message,
                        'status': status,
                        'data': result
                    }
                ), 
                headers={'Content-Type': 'application/json'}
            )
    @api.model
    def res_json_meta(self, result, status, message, meta):
        return request.make_response(
                json.dumps(
                    {
                        'message': message,
                        'status': status,
                        'data': result,
                        'meta': meta
                    }
                ), 
                headers={'Content-Type': 'application/json'}
            )