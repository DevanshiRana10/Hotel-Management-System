from odoo import fields,api,models

class Season(models.Model):
    _name = "season"
    _description = "This is the Room Type model"
    _rec_name = "name"

    name = fields.Char('Name')
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    non_refundable = fields.Boolean(string='Refundable')