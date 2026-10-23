from odoo import fields,api,models

class HotelService(models.Model):
    _name = "hotel.service"
    _description = "This is the hotel service model"
    _rec_name = "name"

    name = fields.Char('Name of service')
    # for now only create lunch service(Resturant)
    