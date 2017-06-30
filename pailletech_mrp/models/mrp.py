# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c)
#    2016 Open Architects Consulting SPRL - Houssine BAKKALI
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _

class StockMove(osv.osv):
    _inherit = 'stock.move'

    _columns = {
        'production_building_block_id': fields.many2one('mrp.production', 'Production Order for Building Blocks', select=True, copy=False),
    }

class mrp_production(osv.osv):
    _inherit = 'mrp.production'
    
    _columns = {
        'building_blocks': fields.one2many('stock.move', 'production_building_block_id', 'Building Blocks',
            domain=[('state', 'not in', ('done', 'cancel'))], readonly=True, states={'draft': [('readonly', False)]}),
    }
    
    def _prepare_lines(self, cr, uid, production, properties=None, context=None):
        result = super(mrp_production,self)._prepare_lines(cr, uid, production, properties, context)
        for move_line in production.building_blocks:
            result[0].append({
                        'name': move_line.product_id.name,
                        'product_id': move_line.product_id.id,
                        'product_qty': move_line.product_uom_qty,
                        'product_uom': move_line.product_uom.id,
                        'product_uos_qty': move_line.product_uos_qty,
                        'product_uos': move_line.product_uos and move_line.product_uos.id or False,
                    })
        return result
    
    def product_id_change(self, cr, uid, ids, product_id, product_qty=0, context=None):
        vals = super(mrp_production,self).product_id_change(cr, uid, ids, product_id, product_qty, context)
        product = self.pool.get('product.template').browse(cr, uid, product_id)
        vals['domain'] = {'product_uom': [('category_id','=',product.uom_id.category_id.id)]}
        
        return vals
    
class stock_move(osv.osv):
    _inherit = "stock.move"
    
    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False, loc_dest_id=False, partner_id=False):
        vals = super(stock_move,self).onchange_product_id(cr, uid, ids, prod_id, loc_id, loc_dest_id, partner_id)
        product_id = self.pool.get('product.template').browse(cr, uid, prod_id)
        vals['domain'] = {'product_uom': [('category_id','=',product_id.uom_id.category_id.id)]}
        
        return vals
