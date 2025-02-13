from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property Offer"
    _order = "price desc"

    price = fields.Float(string="Offer Price", required=True)
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string="Status",
        required=True,
        copy=False,
        default='refused'
    )
    name = fields.Char(string="Reference", compute="_compute_name", store=True)
    description = fields.Text(string="Description")  # ✅ ADD THIS FIELD
    partner_id = fields.Many2one('res.partner', string="Buyer", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True, ondelete="cascade")
    validity = fields.Integer(string="Validity (days)", default=15)
    date_deadline = fields.Date(string="Deadline", compute="_compute_date_deadline", store=True)

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for offer in self:
            offer.date_deadline = (offer.create_date or fields.Date.today()) + timedelta(days=offer.validity)

    @api.constrains("price")
    def _check_positive_price(self):
        for offer in self:
            if offer.price <= 0:
                raise ValidationError("The offer price must be greater than zero.")

    @api.onchange("price")
    def _onchange_price(self):
        if self.property_id and self.price < self.property_id.selling_price:
            return {
                'warning': {
                    'title': "Low Offer Warning",
                    'message': "The offer is below the selling price of the property."
                }
            }

    @api.depends("partner_id", "property_id")
    def _compute_name(self):
        for offer in self:
            offer.name = f"Offer from {offer.partner_id.name} for {offer.property_id.name}" if offer.partner_id and offer.property_id else "New Offer"
