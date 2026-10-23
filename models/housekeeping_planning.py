from odoo import fields, api, models

class HousekeepingPlanning(models.Model):
    _name = "housekeeping.planning"
    _rec_name = ""
    _description = ''

    name = fields.Char()
    staff = fields.Many2one('house.keeping.staff',string='Staff')
    maintenance_type_ids = fields.Many2many('house.keeping.maintenance.type')
    room_ids = fields.Many2many('hotel.room')