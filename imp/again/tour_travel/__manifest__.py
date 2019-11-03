# -*- coding: utf-8 -*-
{
    'name': "tour_travel",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_crm', 'product', 'purchase', 'crm', 'stock', 'account','mail'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        
#         'views/views.xml',
            'reports/report_attendee_declaration.xml',
            'reports/report_saleorder.xml',
            'views/account_move_view.xml',
            'views/crm_view.xml',
            'views/hotel_reservation_view.xml',
            'views/hotel_view.xml',
            'views/ir_attachment_view.xml',
            'views/passport_booking_view.xml',
            'views/passport_view.xml',
            'views/purchase_order_view.xml',
            'views/res_partner_view.xml',
            'views/sale_order_view.xml',
            'views/stock_picking_view.xml',
            'views/tour_date_view.xml',
            'views/tour_view.xml',
            'views/transport_view.xml',
            'views/visa_booking_view.xml',
            'views/visa_view.xml',
            'wizard/report_attendee_declaration_view.xml',
        'views/actions.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}