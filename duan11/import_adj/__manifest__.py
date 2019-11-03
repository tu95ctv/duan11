# -*- coding: utf-8 -*-
{
    'name': "import_adj",

    'summary': """
        import_adj""",

    'description': """
        import_adj
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','importexcel'],#goc
#     'depends': ['base','importexcel', 'sale_crm', 'product', 'purchase', 'crm', 'stock', 'account'],#cho tour_travel
#     'depends': ['base','importexcel', 'sale_crm', 'product', 'purchase', 'crm', 'stock', 'account'],#goc

#     'depends': ['base','stock'],
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
#         'cu/views/ir_model_fields_import.xml',
#         'cu/views/ir_model_import.xml',
        'views/model_gen.xml',
        'views/fields_import2.xml',
        'views/fields_import.xml',
        'views/model_import.xml',
        'views/action_import.xml',
        'views/menu_import.xml',
        'views/view_import.xml',
        'views/menu.xml',
        
        'views/ihr_importexcel.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}