from odoo import models, fields, api

class transaksi(models.Model):
    _name = 'perpustakaan.transaksi'
    _description = 'class untuk menyimpan data transaksi'

    #attribute
    name = fields.Char('ID Transaksi', size=64, required=True, index=True, readonly=True,states={'draft': [('readonly', False)]})
    member_id = fields.Many2one('perpustakaan.member', string='Member', readonly=True, ondelete="cascade", states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    detail_ids = fields.One2many('perpustakaan.detail', 'transaksi_id', string='Detail')
    total = fields.Integer("Total", compute='_compute_total', store=True, default=0)
    bayar = fields.Selection([('lunas', 'Lunas'),
                             ('hutang', 'Hutang')], required=True,
                            readonly=False, default='hutang', states={'draft': [('readonly', False)]})
    state = fields.Selection(
            [('draft', 'Draft'),
             ('done', 'Done'),
             ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')


    #fungsi hitung total yang harus dibayar

    @api.depends("bayar", "detail_ids", "detail_ids.denda")
    def _compute_total(self):
        for transaksi in self.filtered(lambda s: s.state == 'done'):
            val = {
                "total": 0
            }
            orang = transaksi.member_id.status
            for transaksi in self:
                if transaksi.bayar == 'hutang':
                    for rec in transaksi.detail_ids:
                        if rec.denda > 0:
                            val["total"] += rec.denda + rec.harga_id
                        elif rec.denda <= 0 and orang == 'vip':
                            val["total"] += (rec.harga_id - (rec.harga_id * 0.1))
                        else:
                            val["total"] += rec.harga_id
                else:
                    val["total"] = 0
                transaksi.update(val)


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