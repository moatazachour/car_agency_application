from odoo import models, fields


class CarDamageWizard(models.TransientModel):
    _name = 'car.damage.wizard'
    _description = 'Car Damage Wizard'

    car_id = fields.Many2one('car.car', string="Car", required=True)
    damage_note = fields.Text(string="Damage Description", required=True)

    def action_confirm_damage(self):
        """
        Confirms and updates the car's state to 'damaged'.

        This method updates the state of the car associated with the current record to 'damaged'
        and sets the damage note on the car record based on the current maintenance record.
        """
        self.car_id.write({
            'state': 'damaged',
            'note': self.damage_note,
        })
