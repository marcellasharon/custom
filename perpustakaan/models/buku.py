from odoo import models, fields, api

class buku(models.Model):
    _name = 'perpustakaan.buku'
    _description = 'class untuk menyimpan data buku'

    #attribute
    kode = fields.Char('ISBN', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    name = fields.Char('Judul Buku', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    kategori = fields.Char('Kategori', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    pengarang = fields.Char('Pengarang', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    penerbit = fields.Char('Penerbit', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
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