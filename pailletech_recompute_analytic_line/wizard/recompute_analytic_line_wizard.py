# -*- encoding: utf-8 -*-
from openerp import models, fields, api
from openerp.tools.translate import _

class recompute_analytic_line_wizard(models.TransientModel):
    _name = 'recompute.analytic.line.wizard'
    
    #journal_id = fields.Many2one('account.journal', string='Account Journal')
    from_date = fields.Date(string="From date")
    
    user = fields.Many2one('res.users', string="User")
    
    @api.one
    def recompute_analytic(self):
        if self.from_date:
            move_lines = self.env['account.move.line'].search([('date','>=',self.from_date),('partner_id','=',self.user.partner_id.id)])
        else :
            move_lines = self.env['account.move.line'].search([('partner_id','=',self.user.partner_id.id)])
        for move_line in move_lines:
            move_line.analytic_lines.unlink()
        for move_line in move_lines:
            move_line.create_analytic_lines()
        
        return {'type': 'ir.actions.act_window_close'}
    
    