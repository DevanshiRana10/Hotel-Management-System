from odoo import fields, api, models

class Resturant(models.Model):
    _name = 'resturant'
    _rec_name = "name"

    name = fields.Char(string="Resturant Name")
    hotel_id = fields.Many2one('hotel')
    food_ids = fields.Many2many('food')
    # booking_id = fields.Many2one('room.booking')
    # room_id = fields.Many2one('hotel.room')