from odoo import models, fields, api


class CarMaintenance(models.Model):
    _name = 'car.maintenance'
    _description = 'Car Maintenance'

    car_id = fields.Many2one('car.car', string="Car", required=True)
    damage_note = fields.Text(string="Damage Description", required=True)

    def name_get(self):
        """
        Generates a display name for each record in the format "Maintenance - [Registration Number]".

        This method overrides the default `name_get` method to create a custom display name
        for each maintenance record. The display name is constructed by prefixing "Maintenance - "
        to the car's registration number.
        """

        res = []
        for rec in self:
            name = f"Maintenance - {rec.car_id.registration_number}"
            res.append((rec.id, name))
        return res

    def action_fix_car(self):
        """
        Marks the car as fixed and updates its status to 'available'.

        This method updates the state of the car associated with the current record to 'available'
        and clears the `start_date`, `end_date`, and `customer_id` fields. It then deletes the current
        maintenance record and opens the form view of the repaired car.
        """

        car_id = self.car_id.id

        self.car_id.write({
            'state': 'available',
            'start_date': False,
            'end_date': False,
            'customer_id': False,
        })

        self.unlink()

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'car.car',
            'view_mode': 'form',
            'res_id': car_id,
            'target': 'current',
            'context': self.env.context,
        }

