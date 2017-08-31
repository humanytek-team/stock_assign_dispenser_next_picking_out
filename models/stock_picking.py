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
            picking_type_delivery_order = self.pool.get(
                'ir.model.data').get_object_reference(
                    cr, uid, 'stock', 'picking_type_out')[1]

            domain_search = [
                ('picking_type_id', '=', picking_type_delivery_order),
                ('dispenser_user_id', '=', False),
                ('min_date', '>=', stock_picking_min_date),
                ]
            next_pickings_ids_without_dispenser = self.search(
                cr,
                uid,
                domain_search,
                context=context,
                order='min_date',
                limit=1)

            if next_pickings_ids_without_dispenser:
                next_picking_id = next_pickings_ids_without_dispenser[0]
                self.write(
                    cr,
                    uid,
                    next_picking_id,
                    {'dispenser_user_id': dispenser_user_id},
                    context)

        return do_transfer
