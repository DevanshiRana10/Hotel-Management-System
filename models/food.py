from odoo import fields, api, models

class Food(models.Model):
    _name = 'food'
    _description = "Food"
    _rec_name = "name"


    name = fields.Char(string="Name")
    price = fields.Float(string="Price")
    food_image = fields.Image(store=True, string="")

    def add_food(self):
        print("\n\n\n\n\n\n\n\n\n\n\nFOOD ADDED from KANBAN\n\n\n\n\n\n\n\n\n\n\n")