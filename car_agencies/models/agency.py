from odoo import models, fields, _, api


class CarAgency(models.Model):
    _name = 'car.agency'
    _inherit = 'mail.thread'
    _description = 'Car Agency'

    name = fields.Char(required=True)
    responsible_id = fields.Many2one('res.partner', string="Responsible", required=True, tracking=True)
    car_ids = fields.One2many('car.reference.lines', 'car_agency', string="Cars", tracking=True)
    # brand_ids = fields.One2many('car.brand', 'agency_id', string="Supported Brands")

    def action_view_brands(self):
        return {
            'name': _('Car Brands'),
            'res_model': 'car.brand',
            'view_mode': 'tree,form',
            'context': {'default_agency_id': self.id},
            'domain': [('agency_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }


class CarReferenceLines(models.Model):
    _name = "car.reference.lines"
    _description = "Car Reference Lines"

    car_id = fields.Many2one("car.car", required=True)
    car_number = fields.Char(related="car_id.registration_number")
    car_agency = fields.Many2one("car.agency", string="Car Agency")

    # @api.onchange('car_agency')
    # def _onchange_car_agency(self):
    #     if self.car_agency:
    #         brand_ids = self.car_agency.brand_ids.mapped('id')
    #         return {'domain': {'car_id': [('car_brand_id', 'in', brand_ids)]}}
    #     else:
    #         # If no agency is selected, show no cars
    #         return {'domain': {'car_id': []}}
