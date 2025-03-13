from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    complaint_ids = fields.One2many('complaint.complaint', 'order_id', string="Reclamacions", readonly=False)
