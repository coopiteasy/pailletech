# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import fields, models
import openerp.addons.decimal_precision as dp


class MrpProductProduceLine(models.TransientModel):
    _inherit="mrp.product.produce.line"

    product_qty = fields.Float(string='Quantity (in default UoM)', digits=dp.get_precision('Product Unit of Measure MRP'))
    uom_id = fields.Many2one(related='product_id.uom_id', string='Unit of Measure', help="Default Unit of Measure used for all stock operation.")