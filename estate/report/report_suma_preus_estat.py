from odoo import fields, models, tools

class ReportEstateSumaPreusPerEstat(models.Model):
    _name = 'report.suma.preus.estat'
    _description = "Report suma de preus d'ofertes acceptades per estat i comercial"
    _auto = False
    _rec_name = 'commercial_id'

    commercial_id = fields.Many2one('res.users', string='Comercial', readonly=True)
    state = fields.Char(string='Estat de la propietat', readonly=True)
    suma_preus = fields.Float(string="Suma de preus d'ofertes acceptades", readonly=True)

    def _select(self):
        return """
            MIN(t.id) as id,
            t.salesperson_id as commercial_id,
            CASE t.state
                WHEN 'new' THEN 'Nova'
                WHEN 'offer_received' THEN 'Oferta Rebuda'
                WHEN 'offer_accepted' THEN 'Oferta Acceptada'
                WHEN 'sold' THEN 'Venuda'
                WHEN 'cancelled' THEN 'Cancel·lada'
                ELSE t.state
            END as state,
            COALESCE(SUM(o.price), 0) as suma_preus
        """

    def _from(self):
        return """
            estate_property t
            LEFT JOIN estate_property_offer o ON t.id = o.property_id
        """

    def _group_by(self):
        return """
            t.salesperson_id,
            CASE t.state
                WHEN 'new' THEN 'Nova'
                WHEN 'offer_received' THEN 'Oferta Rebuda'
                WHEN 'offer_accepted' THEN 'Oferta Acceptada'
                WHEN 'sold' THEN 'Venuda'
                WHEN 'cancelled' THEN 'Cancel·lada'
                ELSE t.state
            END
        """

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE or REPLACE VIEW %s as
            SELECT %s
            FROM %s
            GROUP BY %s
        """ % (self._table, self._select(), self._from(), self._group_by()))