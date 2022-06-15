from odoo import models, fields, api

class bukumenu(models.Model):
    _name = 'restaurant.bukumenu'
    _description = 'class untuk menyimpan data menu'

    #attribute
    kode = fields.Char('ID Menu', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    name = fields.Char('Nama Menu', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    kategori = fields.Char('Kategori', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    deskripsi = fields.Char('Deskripsi', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    harga = fields.Integer('Harga', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection(
            [('draft', 'Draft'),
             ('done', 'Done'),
             ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')


    #buat state

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'