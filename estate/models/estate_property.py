from odoo import fields, models, api
from datetime import timedelta

class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Model per a Propietats Immobiliàries'

    name = fields.Char('Nom', required=True)
    description = fields.Text('Descripció')
    postalcode = fields.Char('Codi Postal', required=True)
    availability_date = fields.Date(
        'Data de Disponibilitat',
        default=lambda self: fields.Date.today() + timedelta(days=30)
    )
    expected_price = fields.Float('Preu de Venda Esperat', required=True)
    final_price = fields.Float('Preu de Venda Final', readonly=True, copy=False)
    state = fields.Selection(
        [
            ('new', 'Nova'),
            ('offer_received', 'Oferta Rebuda'),
            ('offer_accepted', 'Oferta Acceptada'),
            ('sold', 'Venuda'),
            ('cancelled', 'Cancel·lada')
        ],
        string='Estat',
        default='new'
    )
    bedrooms = fields.Integer('Nombre de Habitacions', required=True, default=1)

    # Relació Many2one per als tipus (gestió dinàmica)
    property_type_id = fields.Many2one(
        'estate.property.type', 
        string='Tipus de Propietat',
        required=True
    )

    tag_ids = fields.Many2many('estate.property.tag', string='Etiquetes')
    has_elevator = fields.Boolean('Ascensor', default=False)
    has_parking = fields.Boolean('Parking', default=False)
    is_renovated = fields.Boolean('Renovat', default=False)
    bathrooms = fields.Integer('Banys', default=1)
    surface = fields.Float('Superfície (m²)', required=True)
    year_built = fields.Integer('Any de Construcció')
    energy_certificate = fields.Selection(
        [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G')],
        string='Certificat Energètic'
    )
    active = fields.Boolean('Actiu', default=True)

    offer_ids = fields.One2many('estate.property.offer', 'property_id', string='Llistat de Ofertes')
    buyer_id = fields.Many2one('res.partner', string='Comprador', compute='_compute_buyer', store=False)
    salesperson_id = fields.Many2one('res.users', string='Comercial', default=lambda self: self.env.user.id)

    best_offer = fields.Float('Millor Oferta', compute='_compute_best_offer', store=False)
    price_per_m2 = fields.Float('Preu per m²', compute='_compute_price_per_m2', store=False)

    @api.depends('offer_ids.price', 'offer_ids.state')
    def _compute_best_offer(self):
        for record in self:
            valid_offers = record.offer_ids.filtered(lambda offer: offer.state != 'rejected')
            record.best_offer = max(valid_offers.mapped('price'), default=0.0)

    @api.depends('expected_price', 'surface')
    def _compute_price_per_m2(self):
        for record in self:
            record.price_per_m2 = record.expected_price / record.surface if record.surface else 0.0

    @api.depends('offer_ids')
    def _compute_buyer(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda offer: offer.state == 'accepted')
            # Si hi ha més d'una oferta, prenem la primera
            record.buyer_id = accepted_offer[0].partner_id if accepted_offer else False
