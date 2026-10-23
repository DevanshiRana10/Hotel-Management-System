from odoo import fields,api,models

class HotelPolicies(models.Model):
    _name = "hotel.policies"
    _description = "This is the hotel policies model"
    _rec_name = "name"

    name = fields.Char(string="Name")
    hotel_id = fields.Many2one('hotel')
    description = fields.Text(string="Description")