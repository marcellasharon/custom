from odoo import models, fields, api
from odoo.exceptions import UserError
# _ utk translate
class voting(models.Model): #inherit dr Model
    _name = 'idea.voting' #attribut dari class Model (lihat dokumen odoo)
    _description = 'class untuk berlatih ttg voting'
    #_rec_name = 'name'
    _order = 'date desc' #defaultnya adalah id, pengaruhnya saat List view
    #id = fields.Integer() ini otomatis ada di odoo, akan jadi PK, tdk perlu ditulis, smua table odoo

    #membuat attribute field
    name = fields.Char('Number', size=64, required=True, index=True, readonly=True, default='new', states={}) #index true krn field ini yg biasanya
    date = fields.Date('Date Release', default=fields.Date.context_today, readonly=True, help='Please fill the date',
                       states={'draft': [('readonly', False)]})
    state = fields.Selection(
        [('draft', 'Draft'),  # draft--> key, secara technical yang disimpan di dbase, Draft: value yang dilihat user
         ('voted', 'Voted'),
         ('canceled', 'Canceled')], 'State', required=True, readonly=True,  # krn required, sebaiknya dikasi default
        default='draft')  # tuple di dalam list, nama field harus state spy bisa diakses oleh states

    vote = fields.Selection([('yes', 'Yes'),
                             ('no', 'No'),
                             ('abstain', 'Abstain')], required=True,
                            readonly=True,
                            states={'draft': [('readonly', False)]})
    idea_id = fields.Many2one('idea.idea', string='Idea', readonly=True, ondelete="cascade",
                              states={'draft': [('readonly', False)]}, domain="[('state', '=', 'done')]")
    voter_id = fields.Many2one('res.users', 'Voted By', readonly=True, default=lambda self: self.env.user)
    idea_date = fields.Date("Idea date", related='idea_id.date')

    def action_voted(self):
        self.state = 'voted'
    def action_canceled(self):
        self.state = 'canceled'
    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "idea.voting")])
        if not seq:
            raise UserError("idea.voting sequence not found, please create idea.voting sequence")
        for val in vals_list:
            val['name'] = seq.next_by_id(sequence_date=val['date'])

        return super(voting, self).create(vals_list)
