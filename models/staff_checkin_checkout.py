from odoo import fields, api, models

class HousekeepingStaffEntry(models.Model):
    _name = 'house.keeping.staff.entry'
    _description = ""

    staff_id = fields.Many2one('house.keeping.staff')
    check_in = fields.Datetime()
    check_out = fields.Datetime()
    service_id = fields.Many2one('house.keeping.maintenance.service',string="Services")