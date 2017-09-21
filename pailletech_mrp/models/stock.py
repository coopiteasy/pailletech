# -*- coding: utf-8 -*-
#  2015-2017 Coop IT Easy (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import fields, models


class StockHistory(models.Model):
    _inherit = 'stock.history'
    
    uom_id = fields.Many2one(related='product_id.product_tmpl_id.uom_id', string="UoM")
    
class StockQuant(models.Model):
    _inherit = "stock.quant"
    
    uom_id = fields.Many2one(related='product_id.product_tmpl_id.uom_id', string="UoM")