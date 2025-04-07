from odoo import fields, models, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Model per estate.property.offer"

    price = fields.Float('Preu', required=True)
    property_id = fields.Many2one('estate.property', string='Propietat', required=True, ondelete='cascade')
    state = fields.Selection(
        [
            ('new', 'Nova'),
            ('accepted', 'Acceptada'),
            ('rejected', 'Rebutjada')
        ],
        string='Estat',
        default='new',
        required=True
    )
    partner_id = fields.Many2one('res.partner', string='Comprador')
    comments = fields.Text('Comentaris')

    def action_accept(self):
        """Marcar l'oferta com a acceptada i actualitzar el preu final de la propietat."""
        for offer in self:
            offer.state = 'accepted'
            offer.property_id.write({'final_price': offer.price})
