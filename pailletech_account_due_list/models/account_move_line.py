# -*- coding: utf-8 -*-
##############################################################################
#    Copyright (c) 2015 Open Architects Consulting sprl - Houssine BAKKALI
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
from openerp import models, fields, api

class AccountAccount(models.Model):
    _inherit = 'account.account'
    
    pay_and_due_list_account = fields.Boolean(string="Display in account & due list")
    
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    priority = fields.Integer(string="Priority")
    
    advanced_by = fields.Many2one('hr.employee',string="Advanced By")
            
    @api.multi
    @api.depends('date_maturity', 'debit', 'credit', 'reconcile_id',
                 'reconcile_partial_id', 'account_id.reconcile',
                 'amount_currency', 'reconcile_partial_id.line_partial_ids',
                 'currency_id', 'company_id.currency_id')
    def _maturity_residual(self):
        """
            inspired by amount_residual
        """
        for move_line in self:
            if move_line.date_maturity != False:
                sign = (move_line.debit - move_line.credit) < 0 and -1 or 1
                move_line.maturity_residual = move_line.amount_residual * sign
            else:
                move_line.maturity_residual = 0.0