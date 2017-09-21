# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c)
#    2016 Open Architects Consulting SPRL - Houssine BAKKALI
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

{
    "name": "Paille-Tech MRP Extension",
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "author": "Open Architects Consulting SPRL, ",
    "license": "AGPL-3",
    "contributors": [
        "Houssine BAKKALI <houssine.bakkali@gmail.com>",
    ],
    "depends": [
        'mrp',
        'stock',
        'stock_account',
    ],
    "data": [
        'views/mrp_view.xml',
        'views/product_view.xml',
        'views/stock_view.xml',
        'wizard/mrp_produce_view.xml',
    ],
    "installable": True,
}
