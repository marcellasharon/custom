from odoo import models, fields, api, _

class wizkelas(models.TransientModel):
    _name = 'wiz.restaurant.kelas'
    _description = 'class untuk menyimpan data kelas dan restaurant'

    kelas_id = fields.Many2one('restaurant.kelas', string='Kelas')
    tanggal = fields.Float(string='Tanggal dan Jam')
    customer_id = fields.Many2one(related='kelas_id.customer_id')
    # detail_ids = fields.One2many('restaurant.detail', 'orders_id', string='Detail')
    # total_qty = fields.Integer("Total Qty", compute='_compute_total_qty', store=True, default=0)
    # total_harga = fields.Integer("Total Harga", compute='_compute_total_harga', store=True, default=0)

    line_ids = fields.One2many('wiz.restaurant.kelas.lines', 'wiz_header_id', string='Detail')

    def action_wiz_restaurant(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Restaurant Kelas'),
            'res_model': 'wiz.restaurant.kelas',
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
        line_ids = self.env['wiz.restaurant.kelas.lines']
        for rec in self.kelas_id.line_ids:
            line_ids += self.env['wiz.restaurant.kelas.lines'].new({
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
    _name = 'wiz.restaurant.kelas.lines'
    _description = 'class untuk menyimpan data nilai suatu kelas'

    wiz_header_id = fields.Many2one('wiz.restaurant.kelas', string='Kelas')
    bukumenu_id = fields.Many2one('restaurant.bukumenu', string='Buku Menu', ondelete="restrict")
    harga_id = fields.Integer("Harga", related='bukumenu_id.harga', store=True, default=0)

    qty = fields.Integer("Qty", readonly=False, store=True, default=0)
    # subtotal = fields.Integer("Subtotal", compute="_compute_subtotal", store=True, default=0)
    ref_kelas_lines_id = fields.Many2one('restaurant.kelas.lines')
