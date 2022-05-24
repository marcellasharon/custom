from odoo import models, fields, api

class detail(models.Model):
    _name = 'perpustakaan.detail'
    _description = 'class untuk menyimpan data detail transaksi'

    #attribute
    kode = fields.Char('ID Detail', size=64, required=True, index=True, readonly=False)
    tanggal_pinjam = fields.Date('Tanggal Pinjam', default=fields.Date.context_today, readonly=False, help='Please fill the date')
    tanggal_kembali = fields.Date('Tanggal Kembali', default=fields.Date.context_today, readonly=False, help='Please fill the date')
    selisih_tanggal = fields.Integer("Keterlambatan Hari", compute="_compute_selisih", store=True, default=0)
    denda = fields.Integer("Denda", compute="_compute_denda", store=True, default=0)
    transaksi_id = fields.Many2one('perpustakaan.transaksi', string='ID Transaksi', readonly=False, ondelete="cascade", states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    buku_id = fields.Many2one('perpustakaan.buku', string='Buku', readonly=False, ondelete="cascade", states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    harga_id = fields.Integer("Harga", related='buku_id.harga', store=True, default=0)

    #fungsi utk hitung selisih tanggal

    @api.depends("tanggal_pinjam", "tanggal_kembali")
    def _compute_selisih(self):
        for rec in self:
            selisih_tanggal = 0
            if rec.tanggal_kembali < rec.tanggal_pinjam:
                raise ValueError('Tanggal kembali harus lebih besar dari tanggal pinjam')
            else:
                selisih_tanggal = ((rec.tanggal_kembali - rec.tanggal_pinjam).days) + 1
                if selisih_tanggal <= 5:
                    selisih_tanggal = 0
                else:
                    selisih_tanggal = selisih_tanggal - 5
            rec.selisih_tanggal= selisih_tanggal


    # fungsi utk hitung denda

    @api.depends("selisih_tanggal")
    def _compute_denda(self):
        for rec in self:
            denda = 0
            if rec.selisih_tanggal > 5:
                denda = rec.selisih_tanggal * 1000
            else:
                denda = 0
            rec.denda = denda

