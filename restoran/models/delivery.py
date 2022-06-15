from odoo import models, fields, api

class delivery(models.Model):
    _name = 'restoran.delivery'
    _description = 'class untuk menyimpan data delivery'

    #attribute
    kode = fields.Char('ID Delivery', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    arrival_time = fields.Float(string='Arrival Time')
    departure_time = fields.Float(string='Departure Time')
    employee_id = fields.Many2one('restoran.employee', string='Employee', readonly=True, ondelete="cascade",
                                  states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    kelas_id = fields.Many2one('restoran.kelas', string='Order', readonly=True, ondelete="cascade",
                                  states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    status = fields.Selection([('perjalanan', 'Perjalanan'),
                               ('sampai', 'Sampai')], required=True, readonly=False, default='basic',
                              states={'draft': [('readonly', False)]})
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