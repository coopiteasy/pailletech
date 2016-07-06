# -*- coding: utf-8 -*-
from openerp.osv import fields, osv

class sale_order(osv.Model):
    _inherit = "sale.order"
    
    _columns = {
        'partner_shipping_id': fields.many2one('res.partner', 'Delivery Address', readonly=True, required=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'manual': [('readonly', False)]}, help="Delivery address for current sales order."),
    }