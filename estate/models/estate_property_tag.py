from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tag"

    name = fields.Char(string="Tag Name", required=True, unique=True)
    color = fields.Integer(string="Color")  # Ensure this field exists
