# -*- coding: utf-8 -*-
# Copyright 2017 Humanytek - Manuel Marquez <manuel@humanytek.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html)

from openerp import api, models


class StockDispenser(models.Model):
    _inherit = 'stock.dispenser'

    @api.multi
    def toggle_active(self):

        super(StockDispenser, self).toggle_active()

        StockPicking = self.env['stock.picking']

        for record in self:

            active_pickings = record.stock_picking_ids.filtered(
                lambda picking: picking.state in
                ['assigned', 'partially_available'])

            if record.active and not active_pickings:

                domain_search = [
                    ('picking_type_code', '=', 'outgoing'),
                    ('dispenser_user_id', '=', False),
                    ('state', 'in', ['assigned', 'partially_available']),
                    ]
                picking_without_dispenser = StockPicking.search(
                    domain_search,
                    order='min_date',
                    limit=1)

                if picking_without_dispenser:
                    picking_without_dispenser.dispenser_user_id = record

                else:
                    record.active_and_free = True
