# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRLfs
#         Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models

class StockMove(models.Model):
    _inherit = "stock.move"

    inverted_prod_order_id = fields.Many2one('mrp.production',
                                             string="Inverted prod order")
