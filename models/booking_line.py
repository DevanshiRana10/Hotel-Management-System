from odoo import fields,api,models

class BookingOrderLines(models.Model):
    _name = "book.order.lines"
    _description = "this is booking order lines"

    
    room_id = fields.Many2one('hotel.room', string="Room")
    booking_id = fields.Many2one('room.booking', string="Booking")

    check_in = fields.Date(string="Check In",related='booking_id.check_in')
    check_out = fields.Date(related='booking_id.check_out')

    room_type = fields.Many2one(string="Room Type", related='room_id.room_type_id')
    floor = fields.Integer(string='Floor')

    price = fields.Float(string="Price", store=True)
    discount_type = fields.Selection([('percentage','Percentage'),('fixed','Fixed')])
    discount = fields.Float(string="Discount")
    amount = fields.Float(string="Amount", compute="calc_amount",store=True)

    @api.depends('room_id','room_id.room_type_id','booking_id','booking_id.check_in','booking_id.check_out','booking_id.total_days')
    def calc_amount(self):
        for rec in self:
            if not rec.room_id or not rec.check_out or not rec.check_in:
                rec.price = 0.0
                rec.amount = 0.0
                rec.discount = 0.0
                print('111111111111111111111111111111')
                continue

            base_price = rec.room_id.price
            total_amount = base_price
            discount_value = 0.0
            room_type = rec.room_id.room_type_id
            hotel = rec.booking_id.hotel_id.id

            pricelist = self.env['pricelist.item'].search([
                ('hotel_id','=', hotel),
                ('room_type_id','=',room_type.id),
                ('start_date','<=',rec.check_in),
                ('end_date','>=', rec.check_out)],limit=1)
            
            if pricelist:
                # print("\n\nttttttttttttttttttttt",pricelist.select_pl)
                # rec.discount_type = pricelist.select_pl
                base_price = pricelist.base_price
                total_amount = pricelist.final_price


                if pricelist.select_pl == 'discount':
                    rec.discount_type = pricelist.discount_type

                    if pricelist.discount_type == 'percentage':
                        discount_value = pricelist.discount_percentage

                    elif pricelist.discount_type == 'fixed':
                        if base_price:
                            discount_value = (pricelist.discount_fixed / base_price) * 100
                        else:
                            discount_value = 0.0

                elif pricelist.select_pl == 'season':
                    if base_price:
                        increase = pricelist.increase_price
                        discount_value = -((increase / base_price) * 100)
                    else:
                        discount_value = 0.0

            
            rec.price = base_price
            rec.amount = total_amount
            rec.discount = discount_value

    def add_meal(self):
            print('\n\n\n\n\n\nMEAL ADDED\n\n\n\n')
            return {
            'type': 'ir.actions.act_window',
            'name': 'Food Kanban',
            'res_model': 'food',
            'view_mode': 'kanban',
            'target': 'new',
            'views': [(self.env.ref('hotel_management_module.food_kanban').id, 'kanban')],
            'flags': {'form': {'action_buttons': True, 'create': False, 'edit': False},'search_view': True}
            
            }

            # @api.onchange('room_id')
    # def onchange_room_id(self):
    #     if self.room_id:
    #         self.room_type = self.room_id.room_type_id.name
    #         self.floor = self.room_id.floor