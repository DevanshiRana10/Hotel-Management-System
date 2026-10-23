from odoo import api,fields,models

class RoomSpecification(models.Model):
    _name = "room.specification"
    _description = "This is the Specification Model"

    name = fields.Char(string="Name")