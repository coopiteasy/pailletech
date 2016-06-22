# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _

class recompute_signed_amount_wizard(models.TransientModel):
    _name = 'recompute.maturity.residual.wizard'
    
    @api.one
    def recompute_maturity_residual(self):
        move_lines = self.env['account.move.line'].search([])
        for move_line in move_lines:
            if move_line.date_maturity != False:
                sign = (move_line.debit - move_line.credit) < 0 and -1 or 1
                move_line.maturity_residual = move_line.amount_residual * sign
            else:
                move_line.maturity_residual = 0.0
        
        
        return {'type': 'ir.actions.act_window_close'}
    
    