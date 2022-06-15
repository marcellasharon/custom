from odoo import models, fields, api

class detail(models.Model):
    _name = 'restoran.detail'
    _description = 'class untuk menyimpan data detail orders'

    #attribute
    kode = fields.Char('ID Detail', size=64, required=True, index=True, readonly=False)
    qty = fields.Integer("Qty", readonly=False, store=True, default=0)
    subtotal = fields.Integer("Subtotal", compute="_compute_subtotal", store=True, default=0)
    #subtotal = fields.Integer("Subtotal", readonly=False, store=True, default=0)
    orders_id = fields.Many2one('restoran.orders', string='ID Orders', readonly=False, ondelete="cascade", states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    bukumenu_id = fields.Many2one('restoran.bukumenu', string='Buku Menu', readonly=False, ondelete="cascade", states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    harga_id = fields.Integer("Harga", related='bukumenu_id.harga', store=True, default=0)

    #fungsi utk hitung selisih tanggal

    @api.depends("qty", "harga_id")
    def _compute_subtotal(self):
        for rec in self:
            subtotal = 0
            if rec.qty > 0:
                subtotal = rec.qty * rec.harga_id
            else:
                subttoal = 0
            rec.subtotal = subtotal


    # # fungsi utk hitung denda
    #
    # @api.depends("selisih_tanggal")
    # def _compute_denda(self):
    #     for rec in self:
    #         denda = 0
    #         if rec.selisih_tanggal > 5:
    #             denda = rec.selisih_tanggal * 1000
    #         else:
    #             denda = 0
    #         rec.denda = denda
