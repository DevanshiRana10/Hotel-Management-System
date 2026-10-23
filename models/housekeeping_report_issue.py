from odoo import fields, api, models

class HousekeepingReportIssue(models.Model):
    _name = 'housekeeping.report.issue'
    _description = ""

    issue_date = fields.Date()
    guest_id = fields.Many2one('hotel.guest')
    hotel_id = fields.Many2one('hotel')
    room_id = fields.Many2one('hotel.room')
    maintenace_type_id = fields.Many2one('house.keeping.maintenance.type')
    status = fields.Selection([('pending','Pending'),('done','Done')])
    description = fields.Text('Description')
    staff_id = fields.Many2one("house.keeping.staff", string="Staff Member")

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        
        self.env["housekeeping.report"].create({
            "issue_date":self.issue_date,
            "guest_id":self.guest_id.id,
            "hotel_id":self.hotel_id.id,
            "room_id":self.room_id.id,
            "maintenace_type_id":self.maintenace_type_id.id,
            "status":self.status,
            "description":self.description,
            "staff_id":self.staff_id.id,
        })

        return res