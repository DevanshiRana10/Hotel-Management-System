from odoo import fields,api,models

class RoomPrice(models.Model):
    _name = "room.price"
    _description = "This is the Room Type model"
    # _rec_name = ""

    name = fields.Char()
    pricelist_item_ids = fields.One2many('pricelist.item','pricelist_id')
    hotel_id = fields.Many2one('hotel',string="Hotel")
    