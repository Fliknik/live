# -*- coding: utf-8 -*-
{
    'name': "Multi Payments",

    'summary': """
        Multi Payments""",

    'description': """
       Add Multi payments under account.move 
    """,

    'author': "Viltco",
    'website': "http://www.viltco.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','purchase','account','sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        "security/security.xml",
        'views/views.xml',
        'views/templates.xml',
        'report/multi_payment_report.xml',
        'report/multi_payment_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
