# -*- coding: utf-8 -*-
# Copyright 2020 Coop IT Easy SCRLfs
#         Houssine BAKKALI <houssine@coopiteasy.be>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP Production inverse stock moves",
     'description': """
        This module allows to inverse the stock moves of 
        a production order which has been terminated. It will
        put the produced product to the scrap and created all
        the stock moves from production to stock
     """,
    "version": "8.0.1.0.0",
    "category": "Manufacturing",
    "author": "Coop IT Easy SCRLfs, ",
    "website": "www.coopiteasy.be",
    "license": "AGPL-3",
    "depends": [
        'mrp',
    ],
    "data": [
        'views/mrp_view.xml',
    ],
    "installable": True,
}
