# -*- coding: utf-8 -*-
# Copyright 2016 - Today Coop IT Easy SCRLfs
#         Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

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
        'mrp_project',
        'mrp_production_inverse_moves'
    ],
    "data": [
        'data/pailletech_mrp_data.xml',
        'views/mrp_view.xml',
        'views/product_view.xml',
        'views/stock_view.xml',
        'wizard/mrp_produce_view.xml',
        'report/report_mrporder.xml',
    ],
    "installable": True,
}
