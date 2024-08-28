from odoo import models, fields, api


class CarMaintenance(models.Model):
    _name = 'car.maintenance'
    _description = 'Car Maintenance'

    car_id = fields.Many2one('car.car', string="Car", required=True)
    damage_note = fields.Text(string="Damage Description", required=True)

    def name_get(self):
        res = []
        for rec in self:
            name = f"Maintenance - {rec.car_id.registration_number}"
            res.append((rec.id, name))
        return res


    def action_fix_car(self):
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

        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'title': 'Car Fixed',
        #         'message': 'The car has been marked as fixed and removed from maintenance.',
        #         'type': 'success',
        #     }
        # }

