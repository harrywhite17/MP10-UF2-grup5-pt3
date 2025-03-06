from odoo import models, fields

class ComplaintReason(models.Model):
    _name = 'complaint.reason'
    _description = 'Complaint Reasons'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    type = fields.Selection([('closure', 'Closure'), ('cancellation', 'Cancellation')], string='Type', required=True)