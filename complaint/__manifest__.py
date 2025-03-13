{
 "name": "Reclamacions",
 "version": "1.0",
 "application": True,
 "depends": ["base", "sale", "stock", "account"],
 "data": [
    'security/ir.model.access.csv',
    'views/complaint_views.xml',
    'views/complaint_reason_views.xml',
    'views/complaint_message_views.xml',
    'views/sale_order_views.xml',
 ],
 "installable": True,
 "license": "LGPL-3",
}