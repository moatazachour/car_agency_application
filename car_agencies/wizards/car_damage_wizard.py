from odoo import models, fields


class CarDamageWizard(models.TransientModel):
    _name = 'car.damage.wizard'
    _description = 'Car Damage Wizard'

    car_id = fields.Many2one('car.car', string="Car", required=True)
    damage_note = fields.Text(string="Damage Description", required=True)

    def action_confirm_damage(self):
        self.car_id.write({
            'state': 'damaged',
            'note': self.damage_note,
        })
