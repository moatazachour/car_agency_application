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
        """
        Ensures that the registration number meets specific criteria.

        This method checks the following constraints for the `registration_number` field:
        1. The registration number must be exactly 8 digits long and must consist only of digits.
        2. The registration number must be unique across all records.

        Raises:
            ValidationError: If the registration number does not meet the length requirement,
                             contains non-digit characters, or is not unique.
        """
        for rec in self:
            if len(rec.registration_number) != 8 or not rec.registration_number.isdigit():
                raise ValidationError("Registration number should be positive and contains exactly 8 numbers")
            if self.search_count([('registration_number', '=', rec.registration_number)]) > 1:
                raise ValidationError("The registration number should be unique.")

    def name_get(self):
        """
        Generates a display name for each record in the format "Car Brand - Car Model".

        This method overrides the default name_get method to create a custom display name
        for each record. The display name is constructed by combining the name of the car brand
        and the car model, separated by a hyphen.
        """
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
        """
        Overrides the write method to add a car to the maintenance model if its state is updated to 'damaged'.

        After updating an existing car record, this method checks if the car's state has been changed to 'damaged'.
        If so, it creates a corresponding maintenance record in the `car.maintenance` model,
        including the car ID and any damage note.
        """
        res = super(Car, self).write(vals)
        if 'state' in vals and vals['state'] == 'damaged':
            self.env['car.maintenance'].create({
                'car_id': self.id,
                'damage_note': self.note,
            })
        return res

    def action_set_damaged(self):
        """
        Opens a wizard form to mark the car as damaged.

        This method triggers the display of a form view for the `car.damage.wizard` model,
        allowing the user to mark the car as damaged. The form is presented as a modal window,
        and the current car's ID is passed as the default value for the `car_id` field in the wizard.
        """

        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'car.damage.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_car_id': self.id},
        }
