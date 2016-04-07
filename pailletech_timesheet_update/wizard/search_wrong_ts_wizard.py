# -*- encoding: utf-8 -*-
from openerp.osv import orm, fields
from openerp.tools.translate import _

class search_wrong_ts_wizard(orm.TransientModel):
    _name = 'search.wrong.ts.wizard'
    
    user_id = fields.many2one('res.users', string='User')
    
    def search_wrong_ts(self, cr, uid, ids, context):
        user_obj = self.pool.get('res.users')
        ts_obj = self.pool.get('hr.analytic.timesheet')
        acc_anal_journal = self.pool.get('account.analytic.journal')
        prod_obj = self.pool.get('product.product')
        product_employee = {}
        
        journal_id = acc_anal_journal.search(cr, uid, [('name','=',"Timesheet Journal")])[0]
        product_uom_id = self.pool.get('product.uom').search(cr, uid, [('name','=',"Hour(s)")])[0]
        
        ts_values = {}
        ts_values['journal_id'] = journal_id
        ts_values['to_invoice'] = False
        ts_values['product_uom_id'] = product_uom_id
        
        # force uom of product to time unit
        user_ids = user_obj.search(cr, uid, [])
        uom_vals = {'uom_id':product_uom_id,
                    'uom_po_id':product_uom_id,
                    'uos_id':product_uom_id}
        for user in user_obj.browse(cr, uid, user_ids, context):
            if user.employee_ids and user.employee_ids[0].product_id:
                product = user.employee_ids[0].product_id
                uom_vals['property_account_expense'] = product.property_account_expense.id
                uom_vals['name'] = product.name
                uom_vals['standard_price'] = product.standard_price
                new_prod_id = prod_obj.copy(cr, uid, product.id, uom_vals, context=context)
                self.pool.get('hr.employee').write(cr, uid, user.employee_ids[0].id, {'product_id':new_prod_id}, context)
                prod_obj.unlink(cr,uid, product.id,context)
        
        for user in user_obj.browse(cr, uid, user_ids, context):
            if user.employee_ids and user.employee_ids[0].product_id:
                product = user.employee_ids[0].product_id
                
                ts_values['product_id'] = product.id
                ts_values['general_account_id'] = product.property_account_expense.id
                price = - product.standard_price
                ts_ids = ts_obj.search(cr, uid, [('user_id','=',user.id)])
                for ts in ts_obj.browse(cr, uid, ts_ids, context):
                    if ts.sheet_id == False or ts.sheet_id.state in ['draft', 'new', False]:
                        ts_values['amount'] = ts.unit_amount * price
                        ts_obj.write(cr, uid, ts.id, ts_values, context)
        
        return True
    
    