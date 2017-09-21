# -*- coding: utf-8 -*-
# 2015-2017 Coop IT Easy (<http://www.coopiteasy.be>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    
    parent_analytic_account = fields.Many2one(related='account_id.parent_id', string="Parent Analytic Account")