from odoo import models, fields, api
from datetime import timedelta


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property"

    name = fields.Char(string="Nom", required=True)
    description = fields.Text(string="Descripció")
    postal_code = fields.Char(string="Codi Postal", required=True)
    availability_date = fields.Date(string="Data de Disponibilitat", copy=False,
                                    default=lambda self: fields.Date.today() + timedelta(days=30))
    expected_price = fields.Float(string="Preu de Venda Esperat", required=True)
    selling_price = fields.Float(string="Preu de Venda Final", readonly=True, copy=False)
    best_offer = fields.Float(string="Millor Oferta", compute="_compute_best_offer", store=False)

    state = fields.Selection(
        [('nova', 'Nova'), ('oferta_rebuda', 'Oferta Rebuda'), ('oferta_acceptada', 'Oferta Acceptada'),
         ('venuda', 'Venuda'), ('cancel.lada', 'Cancel·lada')],
        string="Estat", default='nova'
    )

    rooms = fields.Integer(string="Nombre d'Habitacions", required=True)
    property_type_id = fields.Many2one('estate.property.type', string="Tipus")
    tag_ids = fields.Many2many('estate.property.tag', string="Etiquetes")

    has_elevator = fields.Boolean(string="Ascensor", default=False)
    has_parking = fields.Boolean(string="Parking", default=False)
    is_renovated = fields.Boolean(string="Renovat", default=False)

    bathrooms = fields.Integer(string="Banys")
    surface = fields.Float(string="Superfície", required=True)
    price_per_sqm = fields.Float(string="Preu per m²", compute="_compute_price_per_sqm", store=False)

    construction_year = fields.Integer(string="Any de Construcció")
    energy_certificate = fields.Selection(
        [('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G')],
        string="Certificat Energètic"
    )

    active = fields.Boolean(default=True)
    offer_ids = fields.One2many('estate.property.offer', 'property_id', string="Ofertes")
    buyer_id = fields.Many2one('res.partner', string="Comprador", compute="_compute_buyer", store=False)
    salesman_id = fields.Many2one('res.users', string="Comercial", default=lambda self: self.env.user)

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.offer_ids.mapped('price'), default=0)

    @api.depends('selling_price', 'surface')
    def _compute_price_per_sqm(self):
        for record in self:
            record.price_per_sqm = (record.selling_price / record.surface) if record.surface else 0

    @api.depends('offer_ids.status')
    def _compute_buyer(self):
        for record in self:
            accepted_offer = record.offer_ids.filtered(lambda o: o.status == 'accepted')
            record.buyer_id = accepted_offer.partner_id if accepted_offer else False
