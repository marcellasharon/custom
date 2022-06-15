from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    company_type = fields.Selection(selection_add=[('investor', 'Investor')], ondelete={'code': 'cascade'})

    #Attribute
    point = fields.Integer(string="Point Member", store=True)