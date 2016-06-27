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

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'
    
    advanced_by = fields.Many2one('hr.employee', string="Advanced By")
    
    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        """ finalize_invoice_move_lines(move_lines) -> move_lines

            Hook method to be overridden in additional modules to verify and
            possibly alter the move lines to be created by an invoice, for
            special cases.
            :param move_lines: list of dictionaries with the account.move.lines (as for create())
            :return: the (possibly updated) final move_lines to create for this invoice
        """
        for move_line in move_lines:
            if move_line[2]['analytic_account_id'] == False and move_line[2]['tax_code_id'] == False:
                move_line[2]['advanced_by'] = self.advanced_by.id
                #move_lines.update(move_line)
        return move_lines
class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'
    
    advanced_by = fields.Many2one(related='invoice_id.advanced_by',readonly=True)