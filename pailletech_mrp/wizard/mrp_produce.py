# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import fields, models


class MrpProductProduceLine(models.TransientModel):
    _inherit="mrp.product.produce.line"
    
    uom_id = fields.Many2one(related='product_id.uom_id', string='Unit of Measure', help="Default Unit of Measure used for all stock operation.")