from odoo import models, fields, api, _

class wizkelas(models.TransientModel):
    _name = 'wiz.restoran.kelas'
    _description = 'class untuk menyimpan data order dan restoran'

    kelas_id = fields.Many2one('restoran.kelas', string='Order')
    tanggal = fields.Date('Tanggal', default=fields.Date.context_today, readonly=False,
                          help='Please fill the date')
    jam = fields.Float(string='Jam')
    customer_id = fields.Many2one(related='kelas_id.customer_id')
    total_qty = fields.Integer(related='kelas_id.total_qty')
    total_harga = fields.Integer(related='kelas_id.total_harga')
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True,
                             default='draft')

    line_ids = fields.One2many('restoran.kelas.lines', 'kelas_id', string='Detail', readonly=True,
                               states={'draft': [('readonly', False)]})
    # detail_ids = fields.One2many('restaurant.detail', 'orders_id', string='Detail')
    # total_qty = fields.Integer("Total Qty", compute='_compute_total_qty', store=True, default=0)
    # total_harga = fields.Integer("Total Harga", compute='_compute_total_harga', store=True, default=0)

    line_ids = fields.One2many('wiz.restoran.kelas.lines', 'wiz_header_id', string='Detail')

    def action_wiz_restoran(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Restoran Kelas'),
            'res_model': 'wiz.restoran.kelas',
            'view_mode': 'form',
            'target': 'new', 'context': {'active_id': self.id},
        }

    @api.model
    def default_get(self,
                    fields_list):  # ini adalah common method, semacam constructor, akan dijalankan saat create object. Ini akan meng-overwrite default_get dari parent
        res = super(wizkelas, self).default_get(fields_list)
        # res  merupakan dictionary beserta value yang akan diisi, yang sudah diproses di super class (untuk create record baru)
        res['kelas_id'] = self.env.context['active_id']
        return res

    @api.onchange('kelas_id')
    def onchange_orders_id(self):
        if not self.kelas_id:
            return
        vals = []
        line_ids = self.env['wiz.restoran.kelas.lines']
        for rec in self.kelas_id.line_ids:
            line_ids += self.env['wiz.restoran.kelas.lines'].new({
                'wiz_header_id': self.id,
                'bukumenu_id': rec.bukumenu_id.id,
                'ref_kelas_lines_id': rec.id
            })
            # cara membuat record baru di m2m atau o2m
        self.line_ids = line_ids

    def action_confirm(self):
        for rec in self.line_ids:
            rec.ref_kelas_lines_id.qty = rec.qty

class kelas_lines_wiz(models.TransientModel):
    _name = 'wiz.restoran.kelas.lines'
    _description = 'class untuk menyimpan data order'

    wiz_header_id = fields.Many2one('wiz.restoran.kelas', string='Order')
    bukumenu_id = fields.Many2one('restoran.bukumenu', string='Buku Menu', ondelete="restrict")
    harga_id = fields.Integer("Harga", related='bukumenu_id.harga', store=True, default=0)

    qty = fields.Integer("Qty", readonly=False, store=True, default=0)
    subtotal = fields.Integer("Subtotal", compute="_compute_subtotal", store=True, default=0)
    ref_kelas_lines_id = fields.Many2one('restoran.kelas.lines')

    @api.depends("qty", "harga_id")
    def _compute_subtotal(self):
        for rec in self:
            subtotal = 0
            if rec.qty > 0:
                subtotal = rec.qty * rec.harga_id
            else:
                subtotal = 0
            rec.subtotal = subtotal