from odoo import fields,api,models,Command
from odoo.exceptions import ValidationError,UserError


class RoomBooking(models.Model):
    _name = "room.booking"
    _description = "This is the room booking model"
    _rec_name = "booking_id"

    booking_id = fields.Char(string="Booking ID",readonly=True)
    is_available_flag = fields.Boolean()
    adult = fields.Integer(string="Adult")
    children = fields.Integer(string="Children")
    status = fields.Selection([('draft','Draft'),
                               ('confrimed','Confrimed'),
                               ('cancel','Cancel'),
                               ('checked_in','Checked_In'),
                               ('checked_out','Checked Out')], string='Status',default="draft")
    booking_flag = fields.Boolean('Flag')

    check_in = fields.Date(string="Check In Date")
    check_out = fields.Date(string="Check Out Date")
    total_days = fields.Integer(string="Total Days", compute="calc_total_days", store=True)
    show_guest_tab = fields.Boolean(compute="_compute_show_guest_tab", store=True)
    email = fields.Char(string="Email", related='guest_id.email')

# -----------------------------------RELATIONAL FIELDS --------------------------------------------------
    # guest_details_ids = fields.One2many('hotel.guest', 'booking_id', string="Guest Details", required=True)
    guest_ids = fields.Many2many('hotel.guest',string = "Guest Name")
    guest_id = fields.Many2one('hotel.guest',string='Main Guest Details',required=True)
    phone = fields.Char(string="Phone",related='guest_id.phone')
    guest_proof = fields.Selection(string="Guest Proof", related='guest_id.guest_proof')

    hotel_id = fields.Many2one('hotel',string='Hotel')
    room_id = fields.Many2one('hotel.room',string='Room Number')
    service_ids = fields.Many2many('hotel.service',string='Hotel Services')
    bookingorderlines_ids = fields.One2many('book.order.lines', 'booking_id', string="Order Lines")
    price_list_id = fields.Many2one('room.price', string = "Price_list")
    invoice_id = fields.Many2one('account.move')
    # maintenance_id = fields(string="Maintenance Request") #BAKI CHE

# -------------------------------------------SEQUENCE--------------------------------------------------------
    @api.model
    def create(self, vals):
        if vals.get('booking_id', 'New') == 'New':
            vals['booking_id'] = self.env['ir.sequence'].next_by_code('room.booking') or 'New'
        return super(RoomBooking, self).create(vals)
    
    def write(self, vals):
        if vals.get('booking_id', 'New') == 'New':
            vals['booking_id'] = self.env['ir.sequence'].next_by_code('room.booking') or 'New'
        return super(RoomBooking, self).write(vals)


# ----------------------------------------------GUEST COUNT-------------------------------------------------  
    
    
    @api.depends('adult', 'children')
    def _compute_show_guest_tab(self):
        for rec in self:
            rec.show_guest_tab = (rec.adult + rec.children) > 1
    
# ----------------------------------------------TOTAL DAYS-------------------------------------------------  
    
    @api.depends('check_in','check_out','total_days')
    def calc_total_days(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                rec.total_days = (rec.check_out - rec.check_in).days
            else:
                rec.total_days = 0
#-------------------------------------------Extra Room Add Method-------------------------------------------- 
    def action_add_room(self):
        # self.ensure_one()
        self.room_id.is_avail = True
        print(self.room_id.is_avail)
        added_room_ids = self.bookingorderlines_ids.mapped('room_id').ids
        print(added_room_ids,"---------------------------------------------------------------------")
        print(self.hotel_id.id,"//////////////////////////////HOTEL ID")
        return {
            'type': 'ir.actions.act_window',
            'name': 'Select Rooms',
            'res_model': 'hotel.room',
            'view_mode': 'kanban,form',
            'target': 'current',
            'domain': [('id', 'not in', added_room_ids),
                       ('hotel_id','=', self.hotel_id.id),
                       ('status', '=', 'available')],
            'context': {
                'default_booking_id': self.id,
                'booking_mode': True},
            'views': [(self.env.ref('hotel_management_module.hotel_room_view_user_kanban').id, 'kanban'),
                      (self.env.ref('hotel_management_module.hotel_user_room_view_form').id, 'form')],
            'flags': {'form': {'action_buttons': True, 'create': False, 'edit': False},'search_view': True}
            
            }
    def confirm_button(self):
        print('KKKKKKKKKKKKKKKKKKKKKKKKKKkk')
        self.status = 'confrimed'

        print(self.bookingorderlines_ids,"----------------------------------")
        for rec in self.bookingorderlines_ids:
            rec.room_id.status = 'occupied'

        total_guest = self.adult + self.children
        guest_len = len(self.guest_ids)

        if total_guest > 1 and guest_len != total_guest - 1:
            raise ValidationError("Please provide details for all guests.")


      
    @api.onchange('guest_ids')
    def _onchange_guest_details(self):
        total_limit = (self.children + self.adult) - 1
        if len(self.guest_ids) > total_limit:
            raise UserError('GUEST DETAILS OF ALL GUESTS ARE NECESSARY')

    def cancel_button(self):
        print('CANCEL-------------------------------------------')
        for rec in self:
            rec.room_id.status = 'available'
        self.status = 'cancel'




    def create_invoice(self):
        print("INVOICE GENERATED ----------------------------------------------------------")
        if self.invoice_id:
            raise ValidationError("ALREADY INVOICE HAS BEEN GENERATED !!!!\nNote : Please check the invoicing.")
        else:
            journal = self.env["account.journal"].search([('type', '=', 'sale')], limit=1)

            if not journal:
                raise UserError("No Sale journal found. Please configure one.")

            if not self.bookingorderlines_ids:
                raise UserError("No rooms found in booking to generate invoice.")
            print("1111111111111111111111111111111111111111111111111111111111111111111111")

            lines_list = []
            for rec in self.bookingorderlines_ids:
                if not rec.room_id:
                    continue
                lines_list.append(Command.create({
                    'name': rec.room_id.room_number,
                    'quantity': self.total_days or 1,
                    'price_unit': rec.amount,
                }))
            print("2222222222222222222222222222222222222222222222222222222222222222")

            if not lines_list:
                raise UserError("No valid invoice lines could be created.")

            invoice = self.env['account.move'].create({
                'journal_id': journal.id,
                'partner_id': self.guest_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': lines_list,
            })
            print("333333333333333333333333333333333333333333333333333333333333333333")
            self.invoice_id = invoice
            return {
                'name': 'Customer Invoice',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'account.move',
                'res_id': invoice.id,
                'target': 'new',
            }
