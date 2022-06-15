from odoo import models, fields, api

class payment(models.Model):
    _name = 'restaurant.payment'
    _description = 'class untuk menyimpan data payment'

    #attribute
    kode = fields.Char('ID Pembayaran', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    tipe = fields.Selection([('cash', 'Cash'),
                               ('card', 'Card')], required=True, readonly=False, default='basic',
                              states={'draft': [('readonly', False)]})
    status = fields.Selection([('lunas', 'Lunas'),
                               ('belum', 'Belum')], required=True, readonly=False, default='basic', states={'draft': [('readonly', False)]})
    orders_id = fields.Many2one('restaurant.orders', string='ID Orders', readonly=True, ondelete="cascade",
                                states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
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