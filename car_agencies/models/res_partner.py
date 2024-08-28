from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    cin_number = fields.Char(string="CIN Number")
