from odoo import models, fields, api
from odoo import exceptions


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
    invoice_count = fields.Integer(compute='_compute_invoice_count', string='Factures associades')
    delivery_count = fields.Integer(string="Enviaments Associats", compute="_compute_delivery_count")

    resolution = fields.Text(string="Descripció de la Resolució Final")
    reason_id = fields.Many2one('complaint.reason', string="Motiu de Tancament/Cancel·lació")

    def _compute_invoice_count(self):
        for record in self:
            if record.order_id and hasattr(record.order_id, 'invoice_ids'):
                record.invoice_count = len(record.order_id.invoice_ids)
            else:
                record.invoice_count = 0

    @api.depends('order_id')
    def _compute_delivery_count(self):
        for rec in self:
            rec.delivery_count = len(rec.order_id.picking_ids)

    def action_cancel(self):
        for rec in self:
            if not rec.reason_id:
                raise models.ValidationError("S'ha de seleccionar un motiu per a cancel·lar la reclamació.")
            rec.state = 'cancelled'

    def action_close(self):
        for rec in self:
            if not rec.reason_id:
                raise models.ValidationError("S'ha de seleccionar un motiu per a tancar la reclamació.")
            rec.state = 'closed'
            rec.close_date = fields.Datetime.now()
            rec.resolution = "Descripció de la resolució final"

    def action_cancel_sale_command(self):
        """Cancela la orden de venta vinculada."""
        for record in self:
            if record.sale_order_id:
                record.sale_order_id.action_cancel()
            else:
                raise exceptions.UserError("No hay ninguna orden de venta vinculada para cancelar.")

    @api.model
    def create(self, vals):
        if 'order_id' in vals and not vals.get('partner_id'):
            order = self.env['sale.order'].browse(vals['order_id'])
            if order.partner_id:
                vals['partner_id'] = order.partner_id.id
        open_complaints = self.search_count([
            ('order_id', '=', vals.get('order_id')),
            ('state', 'in', ['new', 'in_progress'])
        ])
        if open_complaints > 0:
            raise exceptions.UserError("Ja hi ha una reclamació oberta per aquesta comanda de venda.")
        return super().create(vals)

    def write(self, vals):
        if 'state' in vals and vals['state'] in ['new', 'in_progress']:
            for rec in self:
                open_complaints = self.search_count([
                    ('order_id', '=', rec.order_id.id),
                    ('state', 'in', ['new', 'in_progress']),
                    ('id', '!=', rec.id)
                ])
                if open_complaints > 0:
                    raise exceptions.UserError("Ja hi ha una altra reclamació oberta per aquesta comanda de venda.")
        return super().write(vals)

    def action_reopen(self):
        for rec in self:
            if rec.state not in ['closed', 'cancelled']:
                raise exceptions.UserError("Aquesta reclamació no està tancada ni cancel·lada. No es pot reobrir.")
            open_complaints = self.search_count([
                ('order_id', '=', rec.order_id.id),
                ('state', 'in', ['new', 'in_progress']),
                ('id', '!=', rec.id)
            ])
            if open_complaints > 0:
                raise exceptions.UserError("Ja hi ha una altra reclamació oberta per aquesta comanda de venda.")
            new_state = 'in_progress' if rec.message_ids else 'new'
            rec.state = new_state
            rec.reason_id = False
