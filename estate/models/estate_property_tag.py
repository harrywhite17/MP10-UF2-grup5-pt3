from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Etiquetes per a Propietats Immobiliàries"
    name = fields.Char('Etiqueta', required=True)