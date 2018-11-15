# Copyright 2018 Appcademy SRL
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{'name': 'Maintenance Plan default period',
 'summary': 'Extends preventive maintenance planning',
 'version': '11.0.1.0.0',
 'author': 'Odoo Community Association (OCA), Appcademy SRL',
 'license': 'AGPL-3',
 'category': 'Maintenance',
 'website': 'https://github.com/OCA/maintenance',
 'images': [],
 'depends': [
     'maintenance_plan',
     'hr_maintenance'
     ],
 'data': [
     'security/ir.model.access.csv',
     'security/mnt_access_rules.xml',
     'views/maintenance.xml'
     ],
 'installable': True,
 }
