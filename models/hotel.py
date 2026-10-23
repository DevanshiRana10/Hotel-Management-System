from odoo import fields,api,models

class Hotel(models.Model):
    _name = "hotel"
    _description = "This is the hotel model"
    _rec_name = "name"

    hotel_image = fields.Image(store=True)
    name = fields.Char(string="Name")
    location = fields.Text(string="Location")
    landmark = fields.Char(string="Landmark")
    rating = fields.Selection([('1','1'),
                               ('2','2'),
                               ('3','3'),
                               ('4','4'),
                               ('5','5')],string="Rating")
    
    policy_id = fields.Many2many('hotel.policies',string="Policies")
    amenities_ids = fields.Many2many('hotel.amenities',string="Amenities")
    service_ids = fields.Many2many('hotel.service',string="Service")
    room_ids = fields.One2many('hotel.room','hotel_id',string="Rooms")