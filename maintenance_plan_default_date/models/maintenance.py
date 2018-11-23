# Copyright 2017 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from datetime import timedelta

from odoo import _, api, fields, models

from odoo.exceptions import UserError


class MaintenanceKindExtend(models.Model):

    _inherit = 'maintenance.kind'

    default_period = fields.Integer(string="Default period",
                                    help="Default period for this maintenance",
                                    required=True, default=180)

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    outcome = fields.Selection([
                                   ('c','Conforme'),
                                   ('nc','Non Conforme'),
                                   ('w','Conforme con riserva'),
                                   ('o', 'Fuori servizio')
                                   ],
                               'Esito'
                               )
    equipment_serial_no = fields.Char(string='Numero inventario',
                                     compute='_compute_equip_serial_no')
    maintenance_type = fields.Selection([
                                            ('corrective', 'Corrective'),
                                            ('preventive', 'Preventive'),
                                            ('commissioning', 'Commissioning'),
                                            ('scrap', 'Scrap')
                                        ],
                                        string='Maintenance Type',
                                        default="corrective")


    @api.depends('equipment_id.serial_no')
    def _compute_equip_serial_no(self):
        for request in self:
            request.equipment_serial_no = request.equipment_id.serial_no

class MaintenancePlan(models.Model):

    _inherit = 'maintenance.plan'

    period = fields.Integer(string='Period',
                            help='Days between each maintenance',
                            compute="_compute_default_period")

    @api.depends('maintenance_kind_id.default_period')
    def _compute_default_period(self):
        for plan in self:
           plan.period = plan.maintenance_kind_id.default_period

class MaintenanceEquipment(models.Model):

    _inherit = 'maintenance.equipment'

    maintenance_approaching = fields.Integer(string='Next Mainenance Approaching',
                                         compute="_compute_maintenance_approaching")
    last_outcome = fields.Char(string='Esito ultima manutenzione',
                                compute='_compute_maintenance_outcome')
    last_type = fields.Char(string='Tipo ultima manutenzione',
                                compute='_compute_maintenance_outcome')
    last_kind = fields.Char(string='Categoria ultima manutenzione',
                                compute='_compute_maintenance_outcome')
    last_date = fields.Date(string='Data ultima manutenzione',
                                compute='_compute_maintenance_outcome')

    @api.depends('maintenance_ids.outcome')
    def _compute_maintenance_outcome(self):
        for equipment in self:
            last_maintenance = self.env['maintenance.request'].search([
                ('equipment_id', '=', equipment.id),
                ('outcome', '!=', False),
                ('stage_id.done', '=', True),
                ('close_date', '!=', False)], order="close_date desc", limit=1)
            equipment.last_outcome = last_maintenance.outcome
            equipment.last_kind = last_maintenance.maintenance_kind_id.name
            equipment.last_type = last_maintenance.maintenance_type
            equipment.last_date = last_maintenance.close_date

    @api.depends('next_action_date')
    def _compute_maintenance_approaching(self):
        for equipment in self:
            if (equipment.next_action_date==False):
                equipment.maintenance_approaching = -1000
            else:
                date_now = fields.Date.context_today(self)
                today_date = fields.Date.from_string(date_now)
                datedelta = fields.Date.from_string(equipment.next_action_date) - today_date
                equipment.maintenance_approaching = datedelta.days
