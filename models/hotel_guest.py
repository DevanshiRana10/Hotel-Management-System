from odoo import models,fields,api

class HotelGuest(models.Model):
    _name = "hotel.guest"
    _description = ""
    _rec_name = "name"

    name = fields.Char(string="Name")
    phone = fields.Char(string="Phone Number")
    guest_proof = fields.Selection([('aadhar','Aadhar Card'),
                                    ('passport','Passport'),
                                    ('driving','Driving License')])
    email = fields.Char(string="E-mail")
    
    booking_id = fields.Many2one('room.booking', string="Booking")

    @api.model_create_multi
    def create(self,vals_list):
        res = super().create(vals_list)
        self.env['res.partner'].create({
            'name': self.name
        })
        return res