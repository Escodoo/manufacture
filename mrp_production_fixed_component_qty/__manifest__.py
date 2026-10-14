# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "MRP Production Fixed Component Qty",
    "summary": "Exclude chosen components from being rescaled when a "
    "confirmed Manufacturing Order's quantity to produce changes",
    "version": "18.0.1.0.0",
    "category": "Manufacturing",
    "license": "AGPL-3",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/manufacture",
    "development_status": "Beta",
    "maintainers": ["CristianoMafraJunior"],
    "depends": [
        "mrp",
    ],
    "data": [
        "views/mrp_production_views.xml",
    ],
    "installable": True,
}
