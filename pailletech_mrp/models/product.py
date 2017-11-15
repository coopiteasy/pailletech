# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.exceptions import except_orm, Warning

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _compute_reference_uom(self):
        uom_categ = self.uom_id.category_id
        
        for uom in uom_categ.product_uoms:
            if uom.uom_type == 'reference':
                self.uom_reference = uom.id
                break
        
    uom_reference = fields.Many2one('product.uom', compute="_compute_reference_uom", string="Reference UoM", help="Reference Unit of Measure for the UoM category of this product")
    uom_category = fields.Many2one(related='uom_id.category_id',string="UoM Category", readonly=True, help="Category of this product")
    
class ProductUOMCategory(models.Model):
    _inherit = 'product.uom.categ'
    _order = "name"
    
    product_uoms = fields.One2many('product.uom','category_id', string="Product UoM")
       
class ProductUOM(models.Model):
    _inherit = 'product.uom'

    product_ids = fields.One2many('product.template', 'uom_id', string="Products")

