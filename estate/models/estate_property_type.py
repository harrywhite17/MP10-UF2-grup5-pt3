from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Tipus de Propietats Immobiliàries"

    name = fields.Char('Nom', required=True)