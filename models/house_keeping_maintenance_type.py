from odoo import fields, api, models

class HouseKeepingMaintenancetype(models.Model):
    _name = "house.keeping.maintenance.type"
    _description = "HOuse keeping maintenenance"

    name = fields.Char(string="Name")
    staff_ids = fields.Many2many("house.keeping.staff", string="Staff Member Name")
    checklist_service_ids = fields.Many2many("checklist.service", string="Checklist Service")
    maintenance_service_ids = fields.One2many('house.keeping.maintenance.service','maintenance_type_id',string="Service Provided")