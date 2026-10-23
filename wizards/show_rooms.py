from odoo import api,fields,models
from odoo.exceptions import ValidationError,UserError


class ShowRoomsWizard(models.TransientModel):
    _name = "show.rooms.wizard"
    _description =""

    check_in = fields.Date(string="Check In", required=True)
    check_out = fields.Date(string="Check Out", required=True)
    adult = fields.Integer(string="Adult",default=1)
    children = fields.Integer(string="Children")
    total_person = fields.Integer(string="Total Persons",compute = "total_capacity")

    available_rooms_ids = fields.Many2many('hotel.room')

    hotel_id = fields.Many2one('hotel')
    # room_ids = fields.One2many('hotel.room')

    # domain = ('hotel_id','=', hotel_id)
    @api.depends('children','adult','total_person')
    def total_capacity(self):
        for rec in self:
            rec.total_person = rec.adult + rec.children
    
    @api.depends('check_in','check_out')
    def date_checking(self):
        if self.check_in > self.check_out or self.check_out < self.check_in:
            raise ValidationError('Check-In date should be smaller than Check-Out')

    def confrim_button(self):
        print("////////////////////////////////////////////THIS IS THE WIZARD", self.env.context)
        rooms = self.env['hotel.room'].search([
            ('hotel_id','=',self.hotel_id.id),
            ('status','=','available'),
            ('capacity','>=',self.total_person)
            ])
        
        # kanban_view_id =  self.env.ref('hotel_management_module.hotel_room_view_user_kanban')

        booked_room_ids = self.env['room.booking'].search([('check_in', '<=', self.check_out),('check_out', '>=', self.check_in)])
        print(booked_room_ids,"---------------------------boked eroom uid")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Rooms',
            'res_model': 'hotel.room',
            'view_mode': 'kanban,form',
            'view_ids':[(self.env.ref('hotel_management_module.hotel_room_view_user_kanban').id,'kanban'),(self.env.ref('hotel_management_module.hotel_user_room_view_form').id, 'form')],
            # 'view_ids': [(5, 0, 0),
            #     (0, 0, {'view_mode': 'kanban', 'view_id': 'hotel_management_module.hotel_room_view_user_kanban'}),
            #     (0, 0, {'view_mode': 'form', 'view_id': 'hotel_management_module.hotel_user_room_view_form'}),
            #     ],
            'domain': [('id', 'in', rooms.ids),('id', 'not in', booked_room_ids.ids)],
            'context':{'hotel_id':self.hotel_id.id,
                       'adult':self.adult,
                       'children':self.children,
                       'check_out':self.check_out,
                       'check_in': self.check_in }
        }
    
    # @api.depends("check_in","check_out",'hotel_id')
    # def compute_available_rooms(self):
    #     if self.check_in and self.check_out and self.hotel_id:
    #         available_rooms_filter = self.get_available_rooms_filter(self.check_in, self.check_out,self.hotel_id.id)
    #         self.available_rooms_ids = available_rooms_filter.ids
        

    # def get_available_rooms_filter(self, check_in, check_out,hotel_id):
    #     overlapping_booking = self.env['room.booking'].search([
    #         ('check_in', '<=', check_out),
    #         ('check_out', '>=', check_in)
    #     ])
        
    #     booked_rooms = overlapping_booking.mapped('available_rooms_id')

    #     available_room = self.env['hotel.room'].search([
    #         ('id', 'not in', booked_rooms.ids),
    #         ('status', '=', 'available'),
    #         ('hotel_id','=', hotel_id)
    #     ])
    #     return available_room