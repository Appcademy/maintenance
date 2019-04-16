# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools

class PurchaseOrderExtend(models.Model):
    _inherit = 'purchase.order'
    maintenance_request_id = fields.Many2one(string='Mainenance request',comodel_name='maintenance.request')

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'
    purchase_order_ids = fields.One2many(string='Purchase order',inverse_name='maintenance_request_id',comodel_name='purchase.order')
    thereIsPurchaseOrder = fields.Boolean(compute='_compute_thereIsPurchaseOrder', store=False)

    @api.one
    @api.depends('purchase_order_ids')
    def _compute_thereIsPurchaseOrder(self):
        if len(self.purchase_order_ids) == 0:
            self.thereIsPurchaseOrder = False
        else:
            self.thereIsPurchaseOrder = True

    @api.multi
    @api.depends('purchase_order_ids')
    def goToPurchaseOrder(self):
        self.ensure_one()
        view_id = self.env.ref('purchase.purchase_order_form').id
        for request in self:
            for purchase in request.purchase_order_ids:
                return {
                    'name': 'Purchase order',
                    'type': 'ir.actions.act_window',
                    'view_mode': 'form',
                    'res_model': 'purchase.order',
                    'res_id': purchase.id,
                    'views': [[view_id, 'form']],
                    }

class MaintenanceEquipmentsReport(models.AbstractModel):
    _name = 'report.maintenance_rep_order.equipments_my_repo'

    name=fields.Char(string='Apparecchio', readonly=True)
    vecd=fields.Date(string='Data verifica elettrica',readonly=True)
    veoc=fields.Char(string='Esito verifica elettrica', readonly=True)
    vfcd=fields.Date(string='Data verifica funzionale',readonly=True)
    vfoc=fields.Char(string='Esito verifica funzionale', readonly=True)
    mpcd=fields.Date(string='Data manutenzione preventiva',readonly=True)
    mpoc=fields.Char(string='Esito manutenzione preventiva', readonly=True)
    mpid=fields.Many2one(string='Manutenzione preventiva', comodel_name='maintenance.request')
    veid=fields.Many2one(string='Verifica Elettrica', comodel_name='maintenance.request')
    vfid=fields.Many2one(cstring='Verifica Funzionale', comodel_name='maintenance.request')
    nmpd=fields.Date(string='Prox manutenzione preventiva',readonly=True)
    nved=fields.Date(string='Prox verifica elettrica',readonly=True)
    nvfd=fields.Date(string='Prox verifica funzionale',readonly=True)
    serial_no=fields.Char(string='Numero inventario',readonly=True)
    model=fields.Char(string='Modello', readonly=True)
    location=fields.Char(string='Location', readonly=True)
    partner_ref=fields.Char(string='Matricola', readonly=True)
    partner_id=fields.Many2one(string='Produttore',
                                   comodel_name='res.partner')
    department_id=fields.Many2one(string='UO',
                                  comodel_name='hr.department')
    next_action_date=fields.Date(string='Prossima verifica',readonly=True)

    @api.model
    def get_report_values(self, docids, data=None):
        docs = []
        for did in docids:
            docs.append(self.getLines(did))

        return {
            'doc_ids': docids,
            'doc_model': self._table,
            'docs': docs,
        }

    def getLines(self, id):
        return self.search([('id', '=', id)])

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
                            select maintenance_equipment.id as id,
                            maintenance_equipment.name as name,
                            maintenance_equipment.model as model,
                            maintenance_equipment.location as location,
                            maintenance_equipment.department_id as department_id,
                            maintenance_equipment.partner_ref as partner_ref,
                            maintenance_equipment.partner_id as partner_id,
                            maintenance_equipment.serial_no as serial_no,
                            maintenance_equipment.next_action_date as next_action_date,
                            ve.close_date vecd, ve.outcome veoc,
                            vf.close_date vfcd, vf.outcome vfoc,
                            mp.close_date mpcd, mp.outcome mpoc,
                            ve.id veid,
                            vf.id vfid,
                            mp.id mpid,
                            nve.schedule_date nved,
                            nvf.schedule_date nvfd,
                            nmp.schedule_date nmpd
                            from maintenance_equipment
                            left outer join maintenance_request as vf on
                              vf.equipment_id = maintenance_equipment.id and vf.maintenance_kind_id = 2 and vf.close_date < now()
                            left outer join maintenance_request as ve on
                              ve.equipment_id = maintenance_equipment.id and ve.maintenance_kind_id = 3 and ve.close_date < now()
                            left outer join maintenance_request as mp on
                              mp.equipment_id = maintenance_equipment.id and mp.maintenance_kind_id = 4 and mp.close_date < now()
                            left outer join maintenance_request as nvf on
                              nvf.equipment_id = maintenance_equipment.id and nvf.maintenance_kind_id = 2 and nvf.schedule_date > now()
                            left outer join maintenance_request as nve on
                              nve.equipment_id = maintenance_equipment.id and nve.maintenance_kind_id = 3 and nve.schedule_date > now()
                            left outer join maintenance_request as nmp on
                              nmp.equipment_id = maintenance_equipment.id and nmp.maintenance_kind_id = 4 and nmp.schedule_date > now()
                            )""" % (self._table))
