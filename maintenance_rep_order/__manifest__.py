# -*- coding: utf-8 -*-
{
    'name': "Biomedical Maintenance",

    'summary': """
        Report and model customization for Biomedical and Fratesole""",

    'description': """
        Report and model customization for Biomedical and Fratesole
    """,

    'author': "Appcademy",
    'website': "https://appcademy.tech",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.2',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'maintenance_plan',
        'hr_maintenance',
        'purchase',
        ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/inventory_report.xml',
        'views/maintenance_report.xml',
        'views/maintenance_planner.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
