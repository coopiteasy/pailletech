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
    
    @api.multi
    def write(self, vals):
        if vals.has_key('active'):
            if vals.get('active') == False:
                product_id = self.product_variant_ids.id
                lines = self.env['mrp.bom.line'].search([('product_id','=',product_id)])
                if len(lines) > 0:
                    raise except_orm(_('Error!'),
                    _('The product still referenced in a bill of material line. Please remove the line containing the product before to deactivate it'))
        return super(ProductTemplate,self).write(vals)
            
class ProductUOMCategory(models.Model):
    _inherit = 'product.uom.categ'
    _order = "name"
    
    product_uoms = fields.One2many('product.uom','category_id', string="Product UoM")
       
class ProductUOM(models.Model):
    _inherit = 'product.uom'

    product_ids = fields.One2many('product.template', 'uom_id', string="Products")

