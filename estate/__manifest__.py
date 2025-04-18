{
 "name": "Estate", # The name that will appear in the App list
 "version": "1.0", # Version
 "application": True, # This line says the module is an App, and not a module
 "depends": ["base"], # dependencies
 "data": [
     'security/ir.model.access.csv',
     'views/estate_property_views.xml',
     'views/estate_property_reports_views.xml',
     'views/estate_property_view_filter.xml',
     'report/suma_preus_views.xml',
     'views/estate_menus.xml',
     'report/estate_property_reports.xml',
     'report/estate_property_templates.xml',
 ],
  "installable": True,
 'license': 'LGPL-3',
}