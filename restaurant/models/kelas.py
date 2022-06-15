from odoo import models, fields, api, _

class kelas(models.Model):
    _name = 'restaurant.kelas'
    _description = 'class untuk menyimpan data kelas yang dibuka pada suatu semester'

    kode = fields.Char('ID Orders', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    #name = fields.Char(compute="_compute_name", store=True, recursive=True)
    customer_id = fields.Many2one('restaurant.customer', string='Customer', readonly=True, ondelete="cascade",
                                  states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    tanggal = fields.Float(string='Tanggal dan Jam')
    #detail_ids = fields.One2many('restaurant.detail', 'orders_id', string='Detail')
    total_qty = fields.Integer("Total Qty", compute='_compute_total_qty', store=True, default=0)
    total_harga = fields.Integer("Total Harga", compute='_compute_total_harga', store=True, default=0)
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')


    line_ids = fields.One2many('restaurant.kelas.lines', 'kelas_id', string='Detail', readonly=True,
                                    states={'draft': [('readonly', False)]})
    #_sql_constraints = [('name_unik', 'unique(mk_id, semester, tahun)', _('The class is already exist for the sememster!'))]

    # @api.depends('mk_id.name', 'semester', 'tahun')
    # def _compute_name(self):
    #     for s in self:
    #         s.name = "%s - %s - %s" % (s.mk_id.name, s.semester, s.tahun)

    # fungsi hitung total pesanan

    @api.depends("line_ids", "line_ids.qty")
    def _compute_total_qty(self):
        for orders in self.filtered(lambda s: s.state == 'done'):
            val = {
                "total_qty": 0
            }
            for orders in self:
                for rec in orders.detail_ids:
                    val["total_qty"] += rec.qty
                orders.update(val)

    # fungsi hitung total yang harus dibayar

    @api.depends("line_ids", "line_ids.subtotal")
    def _compute_total_harga(self):
        for orders in self.filtered(lambda s: s.state == 'done'):
            val = {
                "total_harga": 0
            }
            for orders in self:
                for rec in orders.detail_ids:
                    val["total_harga"] += rec.subtotal
                orders.update(val)


    def action_done(self):
        self.state = 'done'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'


    def action_wiz_restaurant(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Restaurant Kelas'),
            'res_model': 'wiz.restaurant.kelas',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }


class kelas_lines(models.Model):
    _name = 'restaurant.kelas.lines'
    _description = 'class untuk menyimpan data nilai suatu kelas'

    kelas_id = fields.Many2one('restaurant.kelas', string='Kelas', ondelete="cascade",
                                states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    bukumenu_id = fields.Many2one('restaurant.bukumenu', string='Buku Menu', readonly=False, ondelete="restrict",
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