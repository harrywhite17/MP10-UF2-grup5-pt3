from odoo import fields, models, api, exceptions

class ComplaintMessage(models.Model):
    _name = 'complaint.message'
    _description = 'Model per estate_property'

    text = fields.Text(required=True)

    author_id = fields.Many2one('res.partner', required=True)

    date = fields.Datetime(default=fields.Datetime.now, required=True)

    complaint_id = fields.Many2one('complaint.complaint', required=True)

    @api.model_create_multi
    def create(self, vals_list):
        """Evitar modificacions posteriors fent que els missatges siguin immutables"""
        records = super().create(vals_list)
        for record in records:
            record._lock_message()
        return records

    def write(self, vals):
        raise exceptions.UserError("No es poden modificar missatges de reclamació.")

    def unlink(self):
        raise exceptions.UserError("No es poden eliminar missatges de reclamació.")