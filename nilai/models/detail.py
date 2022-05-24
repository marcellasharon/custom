from odoo import models, fields, api
# _ utk translate
class detail(models.Model): #inherit dr Model
    _name = 'nilai.detail' #attribut dari class Model (lihat dokumen odoo)
    _description = 'class untuk menyimpan data Nilai Mhs'

    #membuat attribute field
    kode = fields.Char('Kode', size=64, required=True, index=True, readonly=False)

    khs_id = fields.Many2one('nilai.khs', string='khs', readonly=False, ondelete="cascade")
    #mk_id = fields.Many2one('nilai.mk', string='mk', readonly=False, ondelete="cascade", states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    mk_id = fields.Many2one('nilai.mk', string='mk', readonly=False, ondelete="cascade")
                                   # states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    #sks_id = fields.Many2one('nilai.mk', string='sks', readonly=False, ondelete="cascade")
    #mk_ids = fields.Many2one('nilai.mk', string='mk', readonly=True, ondelete="cascade")
    #sks_id = fields.Many2one('mk_ids.sks', string='SKS', readonly=True, ondelete="cascade")
    #mk_id = fields.Many2one('mk_ids.kode', string='Kode MK', readonly=True, ondelete="cascade")
