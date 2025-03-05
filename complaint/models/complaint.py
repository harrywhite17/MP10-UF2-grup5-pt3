from odoo import models, fields, api

class Complaint(models.Model):
    _name = 'complaint.complaint'
    _description = 'Client Complaint'
    
    name = fields.Char(string="Assumpte", required=True)
    description = fields.Text(string="Descripció inicial", required=True)
    state = fields.Selection([
        ('new', 'Nova'),
        ('in_progress', 'En Tractament'),
        ('closed', 'Tancada'),
        ('cancelled', 'Cancel·lada')
    ], string="Estat", default="new", required=True)
    
    order_id = fields.Many2one('sale.order', string="Comanda Associada", required=True)
    partner_id = fields.Many2one('res.partner', string="Client", required=True)
    user_id = fields.Many2one('res.users', string="Usuari Responsable", default=lambda self: self.env.user)
    
    create_date = fields.Datetime(string="Data de Creació", readonly=True, default=fields.Datetime.now)
    write_date = fields.Datetime(string="Data de Modificació", readonly=True)
    close_date = fields.Datetime(string="Data de Tancament", readonly=True)
    
    message_ids = fields.One2many('complaint.message', 'complaint_id', string="Missatges")
    invoice_count = fields.Integer(string="Factures Associades", compute="_compute_invoice_count")
    delivery_count = fields.Integer(string="Enviaments Associats", compute="_compute_delivery_count")
    
    resolution = fields.Text(string="Descripció de la Resolució Final")
    reason_id = fields.Many2one('complaint.reason', string="Motiu de Tancament/Cancel·lació")

    @api.depends('order_id')
    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = len(rec.order_id.invoice_ids)

    @api.depends('order_id')
    def _compute_delivery_count(self):
        for rec in self:
            rec.delivery_count = len(rec.order_id.picking_ids)

    def action_cancel(self):
        for rec in self:
            if not rec.reason_id:
                raise models.ValidationError("S'ha de seleccionar un motiu per a cancel·lar la reclamació.")
            rec.state = 'cancelled'
