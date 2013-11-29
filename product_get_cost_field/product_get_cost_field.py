# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: Alexandre Fayolle
#    Copyright 2012 Camptocamp SA
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
##############################################################################
import logging

from openerp.osv.orm import Model
from openerp.osv import fields
import decimal_precision as dp
_logger = logging.getLogger(__name__)


class Product(Model):
    _inherit = 'product.product'

    def _compute_purchase_price(self, cr, uid, ids,
                                context=None):
        res = {}
        if isinstance(ids, (int, long)):
            ids = [ids]
        for product in self.browse(cr, uid, ids, context=context):
            res[product.id] = product.standard_price
        return res

    def _cost_price(self, cr, uid, ids, field_name, arg, context=None):
        if context is None:
            context = {}
        res = self._compute_purchase_price(cr, uid, ids, context=context)
        _logger.debug("get cost field _cost_price %s, arg: %s, "
                      "context: %s, result:%s",
                      field_name, arg, context, res)
        return res

    def get_cost_field(self, cr, uid, ids, context=None):
        return self._cost_price(cr, uid, ids, '', [], context=context)

    _columns = {
        'cost_price': fields.function(
            _cost_price,
            method=True,
            string='Cost Price',
            digits_compute=dp.get_precision('Sale Price'),
            help="The cost price is the standard price unless you install the "
                 "product_cost_incl_bom module.")
    }
