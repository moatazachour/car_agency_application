from odoo import models, fields


class CarBrand(models.Model):
    _name = 'car.brand'
    _inherit = 'mail.thread'
    _description = 'Car Brand'

    name = fields.Char(string="Car Brand", required=True)
    image = fields.Binary()
    description = fields.Text()
    agency_id = fields.Many2one("car.agency", string="Agency", required=True)
