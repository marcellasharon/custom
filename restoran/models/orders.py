from odoo import models, fields, api

class orders(models.Model):
    _name = 'restoran.orders'
    _description = 'class untuk menyimpan data orders'

    #attribute
    kode = fields.Char('ID Orders', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    customer_id = fields.Many2one('restoran.customer', string='Customer', readonly=True, ondelete="cascade", states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    tanggal = fields.Float(string='Tanggal dan Jam')
    detail_ids = fields.One2many('restoran.detail', 'orders_id', string='Detail')
    total_qty = fields.Integer("Total Qty", compute='_compute_total_qty', store=True, default=0)
    total_harga = fields.Integer("Total Harga", compute='_compute_total_harga', store=True, default=0)
    #delivery_id = fields.Many2one('restaurant.delivery', string='ID Delivery', readonly=True, ondelete="cascade",
                                #states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    state = fields.Selection(
            [('draft', 'Draft'),
             ('done', 'Done'),
             ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    # fungsi hitung total pesanan

    @api.depends("detail_ids", "detail_ids.qty")
    def _compute_total_qty(self):
        for orders in self.filtered(lambda s: s.state == 'done'):
            val = {
                "total_qty": 0
            }
            for orders in self:
                for rec in orders.detail_ids:
                    val["total_qty"] += rec.qty
                orders.update(val)


    #fungsi hitung total yang harus dibayar

    @api.depends("detail_ids", "detail_ids.subtotal")
    def _compute_total_harga(self):
        for orders in self.filtered(lambda s: s.state == 'done'):
            val = {
                "total_harga": 0
            }
            for orders in self:
                for rec in orders.detail_ids:
                    val["total_harga"] += rec.subtotal
                orders.update(val)


    #buat state

    def tes_transaksi(self):
        print("ini di transaksi")
        t = self.env.context.get("keterangan")
        print(t)

    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'