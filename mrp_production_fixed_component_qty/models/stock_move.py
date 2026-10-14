# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class StockMove(models.Model):
    _inherit = "stock.move"

    fixed_qty = fields.Boolean(
        string="Fixed Quantity",
        help="Keep this component's demand as entered, regardless of its "
        "Bill of Materials line. When the quantity to produce of an "
        "already confirmed Manufacturing Order changes, Odoo rescales "
        "every open raw move proportionally -- including components added "
        "by hand, with no Bill of Materials line of their own, that were "
        "never meant to scale with the batch size. Checking this box "
        "excludes this move from that rescaling.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if (
                vals.get("raw_material_production_id")
                and not vals.get("bom_line_id")
                and "fixed_qty" not in vals
            ):
                vals["fixed_qty"] = True
        return super().create(vals_list)
