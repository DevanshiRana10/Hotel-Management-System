from odoo import fields, api, models

class HouseKeepingMaintenanceService(models.Model):
    _name = "house.keeping.maintenance.service"
    _description = "House keeping maintenenance"

    name = fields.Char(string="Name")
    maintenance_date = fields.Date(string='Maintenance Date')
    staff_checklist = fields.Text(string="Staff Check-List")



    maintenance_type_id = fields.Many2one('house.keeping.maintenance.type',string="Service Provided")
    staff_ids = fields.One2many('house.keeping.staff.entry',"service_id", string='Staff')
    room_id = fields.Many2one('hotel.room', string="Rooms")

    status = fields.Selection([('pending','Pending'),('done','Done')])
    # maintenance_type = fields.Selection([('cleaning','Cleaning'),('repairing','Repairing')], string ="Maintenence Type")