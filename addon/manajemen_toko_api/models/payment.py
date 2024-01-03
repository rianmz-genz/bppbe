from odoo import models, fields, api, exceptions

class Payment(models.Model):
    _name = 'new.payment'
    _description = 'Payment'

    user_id = fields.Many2one('res.users', string="User")
    image = fields.Binary()
    summary = fields.Char()
    state = fields.Selection([
        ('diajukan', 'Diajukan'),
        ('accepted', 'Diterima'),
        ('decline', 'Ditolak'),
    ], string='Status', default='diajukan')

    def change_state(self, status):
        self.state = status
        if status == "accepted":
            self.user_id.activate_user()

    @api.model
    def create(self, vals):
        user_id = vals.get('user_id')
        if user_id:
            user = self.env['res.users'].browse(user_id)
            if user.is_active:
                raise exceptions.ValidationError("User is already registered.")
        return super(Payment, self).create(vals)

    def accept(self):
        self.change_state('accepted')

    def decline(self):
        self.change_state('decline')
