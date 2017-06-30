# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.exceptions import except_orm, Warning

class ProductUOM(models.Model):
    _inherit = 'product.uom'
    
    product_ids = fields.One2many('product.template', 'uom_id', string="Products")
    
    @api.multi
    def name_get(self):
        name_list = []
        for product in self:
            display_name = '%s [%s]' % (product.name, product.category_id.name)
            name_list.append((product.id, display_name))
        
        return name_list

# class StockQuant(models.Model):
#     _inherit = 'stock.quant'    
#     
#     product_uom = fields.Many2one(related="product_id.product_tmpl_id.uom_id", comodel='product.uom', string="Unit of Measure")