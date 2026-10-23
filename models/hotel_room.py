from odoo import api,fields,models
from odoo.exceptions import ValidationError,UserError


class HotelRoom(models.Model):
    _name = "hotel.room"
    _description = ""
    _rec_name = "room_number"

    room_image = fields.Image(store=True)
    room_number = fields.Char(string="Room Number")
    floor = fields.Integer(string="Floor Number",required=True)
    status = fields.Selection([('available','Available'),
                               ('occupied','Occupied'),
                               ('maintenance','Maintenance')],default="available")
    price = fields.Float(string="Price", related='room_type_id.base_price', readonly=False)
    capacity = fields.Integer(string="Capacity",related='room_type_id.capacity', readonly=False)

    
    room_specification_ids = fields.Many2many('room.specification', string="Room Specification")
    hotel_id = fields.Many2one('hotel',string="Hotel")
    room_type_id = fields.Many2one('room.type',string="Room Type")
    additional_services_ids = fields.Many2many('hotel.service',string='Services')
    # housekeeping_request_id = fields.Many2one() #baki che
    # housekeeping_request_ids = fields.One2many() #baki che
    is_avail = fields.Boolean(string="Available", default=True)


# @api.multi
# def add_room(self):
#     self.ensure_one()  
#     context = self._context
#     booking_id = context.get('default_booking_id') or context.get('booking_id')

#     if booking_id:
#         # Case: Adding to an existing booking
#         booking = self.env['room.booking'].browse(booking_id)
#         if not booking.exists():
#             raise UserError("Booking not found.")

#         line = self.env['book.order.lines'].create({
#             'room_id': self.id,
#             'booking_id': booking.id,
#         })

#         # Trigger onchange and amount calc
#         line.onchange_room_id()
#         line.calc_amount()

#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'room.booking',
#             'res_id': booking.id,
#             'view_mode': 'form',
#             'target': 'current',
#         }

#     else:
#         # Case: First "Book Now" click → open new booking form pre-filled
#         return {
#             'name': 'New Booking',
#             'view_mode': 'form',
#             'res_model': 'room.booking',
#             'type': 'ir.actions.act_window',
#             'target': 'current',
#             'context': {
#                 'default_check_in': context.get('check_in'),
#                 'default_check_out': context.get('check_out'),
#                 'default_adult': context.get('adult'),
#                 'default_children': context.get('children'),
#                 'default_hotel_id': context.get('hotel_id'),
#                 'default_bookingorderlines_ids': [(0, 0, {
#                     'room_id': self.id,
#                 })]
#             }
#         }



    def add_room(self):
        print("////////////////////////////////////////////This is the Add Room", self._context,self.price)
        # self.is_avail = True
        # print(self.is_avail,"==============")
        context = self._context
        booking_id = context.get('default_booking_id') or context.get('booking_id')
        if booking_id:
            booking = self.env['room.booking'].browse(booking_id)

            line = self.env['book.order.lines'].create({
                    'room_id': self.id,
                    'booking_id': booking.id,
                    # 'price' : self.price,
                    # 'discount':0,
                    # 'booking_id' : booking_id
            })
            # line.onchange_room_id()
            line.calc_amount()

            return {
                'type': 'ir.actions.act_window',
                'res_model': 'room.booking',
                'res_id': booking.id,
                'view_mode': 'form',
                'target': 'current', 
            }

        return {
            'name': 'addroom',
            'view_mode': 'form',
            'res_model': 'room.booking',
            'type': 'ir.actions.act_window',
            'context': {
                'default_check_in': context.get('check_in'),
                'default_check_out': context.get('check_out'),
                'default_adult': context.get('adult'),
                'default_children': context.get('children'),
                'default_hotel_id': context.get('hotel_id'),
                'default_bookingorderlines_ids': [(0, 0, {'room_id': self.id,'price': self.price})]
            }
        }
    
    def make_available(self):
        self.status = 'available'