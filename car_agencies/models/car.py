from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Car(models.Model):
    _name = 'car.car'
    _inherit = 'mail.thread'
    _description = 'Car'

    registration_number = fields.Char(required=True, size=8)
    car_brand_id = fields.Many2one("car.brand", string="Car Brand", required=True)
    car_model = fields.Char(required=True)
    car_image = fields.Binary()
    mileage = fields.Float(tracking=True)
    state = fields.Selection([
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('damaged', 'Damaged')
    ], required=True, default='available', tracking=True)
    start_date = fields.Date(tracking=True)
    end_date = fields.Date(tracking=True)
    agency_id = fields.Many2one('car.agency', string="Agency")
    customer_id = fields.Many2one("res.partner", string="Customer")
    note = fields.Text(string="Damage Note")

    @api.constrains('registration_number')
    def _check_registration_number(self):
        for rec in self:
            if len(rec.registration_number) != 8 or not rec.registration_number.isdigit():
                raise ValidationError("Registration number should be positive and contains exactly 8 numbers")
            if self.search_count([('registration_number', '=', rec.registration_number)]) > 1:
                raise ValidationError("The registration number should be unique.")

    def name_get(self):
        res = []
        for rec in self:
            name = f"{rec.car_brand_id.name} - {rec.car_model}"
            res.append((rec.id, name))
        return res

    @api.model
    def create(self, vals):
        """
        Overrides the create method to automatically add a car to the maintenance model if its state is 'damaged'.

        After creating a new car record, this method checks if the car's state is 'damaged'.
        If so, it creates a corresponding maintenance record in the `car.maintenance` model,
        including the car ID and any damage note.
        """
        res = super(Car, self).create(vals)
        if res.state == 'damaged':
            self.env['car.maintenance'].create({
                'car_id': res.id,
                'damage_note': res.note,
            })
        return res

    def write(self, vals):
        res = super(Car, self).write(vals)
        if 'state' in vals and vals['state'] == 'damaged':
            self.env['car.maintenance'].create({
                'car_id': self.id,
                'damage_note': self.note,
            })
        return res

    def action_set_damaged(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'car.damage.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_car_id': self.id},
        }
