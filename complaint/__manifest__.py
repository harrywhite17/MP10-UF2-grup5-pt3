{
 "name": "Reclamacions",
 "version": "1.0", # Version
 "application": True, # This line says the module is an App, and not a module
 "depends": ["base"], # dependencies
 "data": [
    'security/ir.model.access.csv',
    'views/complaint_views.xml',
    'views/sale_order_views.xml',    
    
 ],
 "installable": True,
 "license": "LGPL-3",
}