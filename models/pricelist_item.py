from odoo import fields,models,api
from odoo.exceptions import UserError, ValidationError

class PricelistItem(models.Model):
    _name = "pricelist.item"
    _description = "Pricelist Item"

    pricelist_id = fields.Many2one('room.price',string="Pricelist")
    hotel_id = fields.Many2one('hotel', related='pricelist_id.hotel_id')

    room_type_id = fields.Many2one('room.type',string="Room Type")
    base_price = fields.Float(string="Base Price", related='room_type_id.base_price' ,required=True,)

    select_pl = fields.Selection([('season','Season'),
                                  ('discount','Discount')])

    season_id = fields.Many2one('season',string="Season")
    start_date = fields.Date(related='season_id.start_date', string="Start Date",readonly=False)
    end_date = fields.Date(related='season_id.end_date', string="End Date",readonly=False)
    increase_price = fields.Float(string="Increase Price(Rs.)")

    discount_type = fields.Selection([('fixed','Fixed'),
                                      ('percentage','Percentage')])
    discount_fixed = fields.Float(string="Discount Fixed")
    discount_percentage = fields.Float(string="Discount Percentage")
    # disc_start_date = fields.Date(string="Start Date")
    # disc_end_date = fields.Date(string="End Date")

    final_price = fields.Float(string="Final Price", compute="_compute_final_price")

    @api.depends('base_price', 'discount_type', 'discount_fixed', 'discount_percentage','select_pl','increase_price')
    def _compute_final_price(self):
        for rec in self:
            for rec in self:
                if rec.select_pl == 'season':
                    rec.final_price = rec.base_price + rec.increase_price
                elif rec.select_pl == 'discount':
                    if rec.discount_type == 'fixed':
                        rec.final_price = rec.base_price - rec.discount_fixed
                    elif rec.discount_type == 'percentage':
                        rec.final_price = rec.base_price - (rec.base_price * rec.discount_percentage / 100)
                    else:
                        rec.final_price = rec.base_price
                else:
                    rec.final_price = rec.base_price
            


    