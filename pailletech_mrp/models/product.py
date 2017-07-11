# -*- coding: utf-8 -*-
from openerp import api, fields, models, _
from openerp.exceptions import except_orm, Warning

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    #@api.depends('uom_id')
    def _compute_reference_uom(self):
        uom_categ = self.uom_id.category_id
        
        for uom in uom_categ.product_uoms:
            if uom.uom_type == 'reference':
                self.uom_reference = uom.id
                break
        
    uom_reference = fields.Many2one('product.uom', compute="_compute_reference_uom", string="Reference UoM", help="Reference Unit of Measure for the UoM category of this product")

class ProductUOMCategory(models.Model):
    _inherit = 'product.uom.categ'
    
    product_uoms = fields.One2many('product.uom','category_id', string="Product UoM")
       
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

