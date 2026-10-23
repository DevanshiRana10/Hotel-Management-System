from odoo import fields,api,models

class HotelAmenities(models.Model):
    _name = "checklist.service"
    _description = "This is the maintenance checklist service"

    name = fields.Char()