from odoo import models, fields, api

class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'
    #attribute
    # kode = fields.Char('ID Customer', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    # name = fields.Char('Nama Customer', size=64, required=True, index=True, readonly=True, states={'draft': [('readonly', False)]})
    # hp = fields.Char('No HP', size=64, required=True, index=True, readonly=True,
    #                    states={'draft': [('readonly', False)]})
    # alamat = fields.Char('Alamat', size=64, required=True, index=True, readonly=True,
    #                    states={'draft': [('readonly', False)]})
    # state = fields.Selection(
    #         [('draft', 'Draft'),
    #          ('done', 'Done'),
    #          ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')
    #
    #
    # # buat state
    #
    # def action_done(self):
    #     self.state = 'done'
    #
    # def action_canceled(self):
    #     self.state = 'canceled'
    #
    # def action_settodraft(self):
    #     self.state = 'draft'