from odoo import fields,api,models

class RoomType(models.Model):
    _name = "room.type"
    _description = "This is the Room Type model"
    _rec_name = "name"

    name = fields.Char('Room Type')
    capacity = fields.Integer('Capacity')
    base_price = fields.Float(string="Base Price")