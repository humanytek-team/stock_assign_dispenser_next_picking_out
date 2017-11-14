# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import random

from openerp.osv import osv


class StockPicking(osv.osv):
    _inherit = 'stock.picking'

    def do_transfer(self, cr, uid, ids, context=None):

        do_transfer = super(StockPicking, self).do_transfer(
            cr, uid, ids, context)

        if do_transfer:
            stock_picking_id = ids[0]
            stock_picking = self.browse(cr, uid, stock_picking_id, context)
            dispenser_user_id = stock_picking.dispenser_user_id.id
            stock_picking_min_date = stock_picking.min_date

            domain_search = [
                ('picking_type_code', '=', 'outgoing'),
                ('dispenser_user_id', '=', False),
                ('min_date', '>=', stock_picking_min_date),
                ('state', 'in', ['assigned', 'partially_available']),
                ]

            StockDispenser = self.pool.get('stock.dispenser')

            dispensers_activated_and_free = StockDispenser.search(
                cr,
                uid,
                [('active_and_free', '=', True)],
                context=context
            )

            next_pickings_ids_without_dispenser = self.search(
                cr,
                uid,
                domain_search,
                context=context,
                order='min_date',
                limit=len(dispensers_activated_and_free)+1)

            if next_pickings_ids_without_dispenser:

                if dispensers_activated_and_free:

                    for pos in range(
                        0, len(next_pickings_ids_without_dispenser)):

                        next_picking_id = \
                            next_pickings_ids_without_dispenser[pos]

                        self.write(
                            cr,
                            uid,
                            next_picking_id,
                            {
                                'dispenser_user_id':
                                dispensers_activated_and_free[pos]
                                },
                            context)

                if len(next_pickings_ids_without_dispenser) == len(
                        dispensers_activated_and_free) + 1:

                    next_picking_id = next_pickings_ids_without_dispenser[-1]
                    self.write(
                        cr,
                        uid,
                        next_picking_id,
                        {'dispenser_user_id': dispenser_user_id},
                        context)

        return do_transfer
