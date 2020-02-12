# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRLfs
#         Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.exceptions import ValidationError

class MRPProduction(models.Model):
    _inherit = 'mrp.production'

    inverted_move_ids = fields.One2many('stock.move',
                                        'inverted_prod_order_id',
                                        string="Inverted stock moves")
    state = fields.Selection(selection_add=[('inverted', 'Inverted')])

    @api.multi
    def action_inverse(self):
        self.ensure_one()
        location_obj = self.env['stock.location']
        move_obj = self.env['stock.move']
        if self.state == 'done':
            if self.move_created_ids2:
                scrap_loc = location_obj.search([('scrap_location', '=', True)])
                for move in self.move_created_ids2:
                    if move.location_dest_id.usage == 'internal':
                        internal_quant = False
                        for quant in move.quant_ids:
                            if quant.location_id.usage == 'internal':
                                internal_quant = quant
                                if internal_quant.qty == 0:
                                    raise ValidationError(_("The produced product quantities has already been moved to the scrap"))
                                else:
                                    move.action_scrap(internal_quant.qty, scrap_loc.id)
                                break
                for move in self.move_lines2:
                    vals = {
                        'name': 'inverted - ' + move.name,
                        'product_id': move.product_id.id,
                        'product_uom': move.product_uom.id,
                        'product_uom_qty': move.product_uom_qty,
                        'product_uos_qty': move.product_uos_qty,
                        'procure_method': 'make_to_stock',
                        'restrict_lot_id': move.restrict_lot_id.id,
                        'procurement_id': move.procurement_id.id,
                        'location_id': move.location_dest_id.id,
                        'location_dest_id': move.location_id.id,
                        'origin': move.origin,
                        'note': move.name,
                        'inverted_prod_order_id': self.id
                    }
                    move = move_obj.create(vals)
                    move.action_done()
            self.state = 'inverted'
        return True