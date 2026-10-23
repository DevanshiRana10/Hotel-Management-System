from odoo import fields, api, models

class HouseKeepingStaff(models.Model):
    _name = "house.keeping.staff"
    _description = "House Keeping Staff"

    name = fields.Char(string="Name")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    age = fields.Integer(string="Age")
    job_profile = fields.Char(string="Job Profile")
    proof_photo = fields.Image(string="Staff Photo")

    hotel_id = fields.Many2one('hotel',string="Hotel")
    room_ids = fields.Many2many('hotel.room')