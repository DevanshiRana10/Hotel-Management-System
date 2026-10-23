from odoo import fields,api,models

class HotelAmenities(models.Model):
    _name = "hotel.amenities"
    _description = "This is the hotel amenities model"
    _rec_name = "name"

    name = fields.Char('Name of Amenity')