# -*- coding: utf-8 -*-
#  2015-2017 Coop IT Easy (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models, api
import openerp.addons.decimal_precision as dp

class StockHistory(models.Model):
    _inherit = 'stock.history'

    uom_id = fields.Many2one(related='product_id.product_tmpl_id.uom_id', string="UoM")


class StockQuant(models.Model):
    _inherit = "stock.quant"

    uom_id = fields.Many2one(related='product_id.product_tmpl_id.uom_id', string="UoM")


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    @api.depends('production_id.project_id',
                 'raw_material_production_id.project_id',
                 'inverted_prod_order_id.project_id')
    def _compute_project_id(self):
        for move in self:
            if move.production_id:
                move.project_id = move.production_id.project_id.id
            elif move.inverted_prod_order_id:
                move.project_id = move.inverted_prod_order_id.project_id.id
            elif move.raw_material_production_id:
                move.project_id = move.raw_material_production_id.project_id.id
            
        
    production_building_block_id =  fields.Many2one('mrp.production', string='Production Order for Building Blocks', select=True, copy=False)
    product_uom_qty = fields.Float(string='Quantity', digits=dp.get_precision('Product Unit of Measure MRP'),
            required=True, states={'done': [('readonly', True)]},
            help="This is the quantity of products from an inventory "
                "point of view. For moves in the state 'done', this is the "
                "quantity of products that were actually moved. For other "
                "moves, this is the quantity of product that is planned to "
                "be moved. Lowering this quantity does not generate a "
                "backorder. Changing this quantity on assigned moves affects "
                "the product reservation, and should be done with care."
        )
    project_id = fields.Many2one(compute='_compute_project_id',
                                 comodel_name='project.project',
                                 string="Project",
                                 store=True)


class MRPBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    description = fields.Char(string='Description')


class MRPProduction(models.Model):
    _inherit = 'mrp.production'
    
    customer_id = fields.Many2one(related='project_id.partner_id', string="Customer")
    building_blocks = fields.One2many('stock.move', 'production_building_block_id', string='Building Blocks',
        domain=[('state', 'not in', ('done', 'cancel'))], readonly=True, copy=True,
        states={'draft': [('readonly', False)]})


    @api.one
    def action_draft(self):
        self.write({'state': 'draft'})
