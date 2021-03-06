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


class mrp_production(osv.osv):
    _inherit = 'mrp.production'
    
    _order = 'name desc'
    
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
        product = self.pool.get('product.product').browse(cr, uid, product_id)
        vals['domain'] = {'product_uom': [('category_id','=',product.product_tmpl_id.uom_id.category_id.id)]}
        
        return vals

    def _make_production_produce_line(self, cr, uid, production, context=None):
        stock_move = self.pool.get('stock.move')
        proc_obj = self.pool.get('procurement.order')
        source_location_id = production.product_id.property_stock_production.id
        destination_location_id = production.location_dest_id.id
        procs = proc_obj.search(cr, uid, [('production_id', '=', production.id)], context=context)
        procurement = procs and\
            proc_obj.browse(cr, uid, procs[0], context=context) or False
        data = {
            'name': production.name,
            'partner_id': production.customer_id.id,
            'date': production.date_planned,
            'product_id': production.product_id.id,
            'product_uom': production.product_uom.id,
            'product_uom_qty': production.product_qty,
            'product_uos_qty': production.product_uos and production.product_uos_qty or False,
            'product_uos': production.product_uos and production.product_uos.id or False,
            'location_id': source_location_id,
            'location_dest_id': destination_location_id,
            'move_dest_id': production.move_prod_id.id,
            'procurement_id': procurement and procurement.id,
            'company_id': production.company_id.id,
            'production_id': production.id,
            'origin': production.name,
            'group_id': procurement and procurement.group_id.id,
        }
        move_id = stock_move.create(cr, uid, data, context=context)
        #a phantom bom cannot be used in mrp order so it's ok to assume the list returned by action_confirm
        #is 1 element long, so we can take the first.
        return stock_move.action_confirm(cr, uid, [move_id], context=context)[0]

class stock_move(osv.osv):
    _inherit = "stock.move"
    
    def onchange_product_id(self, cr, uid, ids, prod_id=False, loc_id=False, loc_dest_id=False, partner_id=False):
        vals = super(stock_move,self).onchange_product_id(cr, uid, ids, prod_id, loc_id, loc_dest_id, partner_id)
        product_id = self.pool.get('product.product').browse(cr, uid, prod_id)
        vals['domain'] = {'product_uom': [('category_id','=',product_id.product_tmpl_id.uom_id.category_id.id)]}
        
        return vals
    
class stock_location_path(osv.osv):
    _inherit = "stock.location.path"
    
    def _prepare_push_apply(self, cr, uid, rule, move, context=None):
        vals = super(stock_location_path, self)._prepare_push_apply(cr, uid, rule, move, context=context)
        vals['partner_id'] = move.partner_id.id
        return vals
