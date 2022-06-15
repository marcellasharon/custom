from odoo import models, fields, api, _

class kelas(models.Model):
    _name = 'restoran.kelas'
    _description = 'class untuk menyimpan data order'

    kode = fields.Char('ID Orders', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    customer_id = fields.Many2one('restoran.customer', string='Customer', readonly=True, ondelete="cascade",
                                  states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    tanggal = fields.Date('Tanggal', default=fields.Date.context_today, readonly=False,
                                help='Please fill the date')
    jam = fields.Float(string='Jam')
    total_qty = fields.Integer("Total Qty", compute='_compute_total_qty', store=True, default=0)
    total_harga = fields.Integer("Total Harga", compute='_compute_total_harga', store=True, default=0)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')


    line_ids = fields.One2many('restoran.kelas.lines', 'kelas_id', string='Detail', readonly=True,
                                    states={'draft': [('readonly', False)]})
    #_sql_constraints = [('name_unik', 'unique(mk_id, semester, tahun)', _('The class is already exist for the sememster!'))]

    # @api.depends('mk_id.name', 'semester', 'tahun')
    # def _compute_name(self):
    #     for s in self:
    #         s.name = "%s - %s - %s" % (s.mk_id.name, s.semester, s.tahun)

    # fungsi hitung total pesanan

    @api.depends("line_ids", "line_ids.qty")
    def _compute_total_qty(self):
        for kelas in self.filtered(lambda s: s.state == 'done'):
            val = {
                "total_qty": 0
            }
            for kelas in self:
                for rec in kelas.line_ids:
                    val["total_qty"] += rec.qty
                kelas.update(val)

    # fungsi hitung total yang harus dibayar

    @api.depends("line_ids", "line_ids.subtotal")
    def _compute_total_harga(self):
        for kelas in self.filtered(lambda s: s.state == 'done'):
            val = {
                "total_harga": 0
            }
            for kelas in self:
                for rec in kelas.line_ids:
                    val["total_harga"] += rec.subtotal
                kelas.update(val)


    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'


    def action_wiz_restoran(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Restoran Kelas'),
            'res_model': 'wiz.restoran.kelas',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }


class kelas_lines(models.Model):
    _name = 'restoran.kelas.lines'
    _description = 'class untuk menyimpan data order'

    kelas_id = fields.Many2one('restoran.kelas', string='Kelas', ondelete="cascade",
                                states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    bukumenu_id = fields.Many2one('restoran.bukumenu', string='Buku Menu', readonly=False, ondelete="restrict",
                                  states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    harga_id = fields.Integer("Harga", related='bukumenu_id.harga', store=True, default=0)

    qty = fields.Integer("Qty", readonly=False, store=True, default=0)
    subtotal = fields.Integer("Subtotal", compute="_compute_subtotal", store=True, default=0)

    # _sql_constraints = [('name_unik', 'unique(kelas_id, mhs_id)', _('The student is already exist!'))]



    @api.depends("qty", "harga_id")
    def _compute_subtotal(self):
        for rec in self:
            subtotal = 0
            if rec.qty > 0:
                subtotal = rec.qty * rec.harga_id
            else:
                subtotal = 0
            rec.subtotal = subtotal