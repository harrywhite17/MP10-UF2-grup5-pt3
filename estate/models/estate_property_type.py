from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Tipus de Propietat'
    _order = 'name'

    name = fields.Char(string='Nom', required=True, unique=True)
    description = fields.Text(string='Descripció')
    property_ids = fields.One2many('estate.property', 'property_type_id', string="Propietats")
