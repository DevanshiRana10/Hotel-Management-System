from odoo import fields, api, models

class HousekeepingReport(models.Model):
    _name = 'housekeeping.report'
    _description = ""

    issue_date = fields.Date()
    guest_id = fields.Many2one('hotel.guest')
    hotel_id = fields.Many2one('hotel')
    room_id = fields.Many2one('hotel.room')
    maintenace_type_id = fields.Many2one('house.keeping.maintenance.type')
    status = fields.Selection([('pending','Pending'),('done','Done')])
    description = fields.Text('Description')
    staff_id = fields.Many2one("house.keeping.staff", string="Staff Member")
