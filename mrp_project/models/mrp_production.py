# -*- coding: utf-8 -*-
# (c) 2014 Daniel Campos <danielcampos@avanzosc.es>
# (c) 2015 Pedro M. Baeza - Serv. Tecnol. Avanzados
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from openerp import models, fields, api, _


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    project_id = fields.Many2one(
        comodel_name="project.project", string="Project",
        readonly=True, states={'draft': [('readonly', False)]},required=True)
    analytic_account_id = fields.Many2one(
        related="project_id.analytic_account_id", store=True)
    
    name = fields.Char(string='Reference', required=True, readonly=True, states={'draft': [('readonly', False)]}, copy=False)
    
    prod_order_seq = fields.Char(string='Production order sequence', readonly=True)
    
    @api.model
    def _prepare_project_vals(self, production):
        # If this production come from a sale order and that order
        # has an analytic account assigned, then project is child of
        # that analytic account
        parent_id = False
        if 'sale_id' in production._fields:
            parent_id = production.sale_id.project_id.id
        return {
            'name': production.name,
            'use_tasks': True,
            'automatic_creation': True,
            'parent_id': parent_id,
        }

    @api.model
    def _prepare_production_task(self, production):
        product = production.product_id
        task_name = "%s::%s%s" % (
            production.name,
            "[%s] " % product.default_code if product.default_code else "",
            product.name)
        task_descr = _("""
        Manufacturing Order: %s
        Product to Produce: [%s]%s
        Quantity to Produce: %s
        Bill of Material: %s
        Planned Date: %s
        """) % (production.name, production.product_id.default_code,
                production.product_id.name, production.product_qty,
                production.bom_id.name, production.date_planned)
        return {
            'mrp_production_id': production.id,
            'user_id': production.user_id.id,
            'reviewer_id': production.user_id.id,
            'name': task_name,
            'project_id': production.project_id.id,
            'description': task_descr
        }

    @api.multi
    def action_in_production(self):
        task_obj = self.env['project.task']
        for record in self:
            task_domain = [('mrp_production_id', '=', record.id),
                           ('workorder', '=', False)]
            tasks = task_obj.search(task_domain)
            if not tasks:
                task_obj.create(self._prepare_production_task(record))
        return super(MrpProduction, self).action_in_production()

    @api.multi
    def action_confirm(self):
        project_obj = self.env['project.project']
        result = super(MrpProduction, self).action_confirm()
        for production in self:
            if not production.project_id:
                origin_prod_order = self.search([('name','=',production.origin)])
                if origin_prod_order.project_id:
                    production.project_id = origin_prod_order.project_id
                else:
                    project_vals = self._prepare_project_vals(production)
                    project = project_obj.create(project_vals)
                    production.project_id = project.id
        return result

    @api.multi
    def unlink(self):
        projects = self.mapped('project_id').filtered('automatic_creation')
        tasks = self.env['project.task'].search(
            [('project_id', 'in', projects.ids)])
        if not tasks.mapped('work_ids'):
            child_tasks = tasks.filtered(lambda x: x.parent_ids)
            child_tasks.unlink()
            (tasks - child_tasks).unlink()
            projects.unlink()
        return super(MrpProduction, self).unlink()


class MrpProductionWorkcenterLine(models.Model):
    _inherit = 'mrp.production.workcenter.line'

    task_ids = fields.One2many(
        comodel_name="project.task", inverse_name="workorder", string="Tasks")
    work_ids = fields.One2many(
        comodel_name="project.task.work", inverse_name="workorder",
        string="Task works")

    @api.multi
    def write(self, vals, update=True):
        for rec in self:
            super(MrpProductionWorkcenterLine, rec.with_context(
                production=rec.production_id)).write(vals, update=update)
        return True

from openerp.osv import osv
    
class procurement_order(osv.osv):
    _inherit = 'procurement.order'
    
    def _prepare_mo_vals(self, cr, uid, procurement, context=None):
        vals = super(procurement_order, self)._prepare_mo_vals(cr, uid, procurement, context)
        prod_ord_obj = self.pool.get('mrp.production')
        if vals.get('origin',False):
            origin_prod_order_id = prod_ord_obj.search(cr, uid,[('name','=',vals['origin'])])
            origin_prod_order = prod_ord_obj.browse(cr, uid, origin_prod_order_id, context)
            if origin_prod_order.project_id:
                vals['project_id'] = origin_prod_order.project_id.id
        
        return vals 