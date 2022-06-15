from odoo import models, fields, api

class employee(models.Model):
    _name = 'restaurant.employee'
    _description = 'class untuk menyimpan data employee'

    #attribute
    kode = fields.Char('ID Employee', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    name = fields.Char('Nama Employee', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    hp = fields.Char('No HP', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    alamat = fields.Char('Alamat', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    role = fields.Selection([('chef', 'Chef'),
                               ('kurir', 'Kurir'),
                               ('kasir', 'Kasir'),
                               ('manager', 'Manager')], required=True, readonly=False, default='basic',
                              states={'draft': [('readonly', False)]})
    state = fields.Selection(
            [('draft', 'Draft'),
             ('done', 'Done'),
             ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')


    # buat state

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'