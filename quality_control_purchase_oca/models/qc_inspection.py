# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class QcInspection(models.Model):

    _inherit = "qc.inspection"

    def _prepare_inspection_header(self, object_ref, trigger_line):
        res = super()._prepare_inspection_header(object_ref, trigger_line)
        # Fill qty when coming from pack operations
        if object_ref and object_ref._name == "purchase.order":
            res["qty"] = object_ref.product_qty
        return res

    @api.depends("object_id")
    def _compute_purchase_id(self):
        for inspection in self:
            if inspection.object_id:
                if inspection.object_id._name == "stock.move":
                    inspection.purchase_id = inspection.object_id.purchase_id
                elif inspection.object_id._name == "purchase.order":
                    inspection.purchase_id = inspection.object_id

    @api.depends("object_id")
    def _compute_product_id(self):
        """Overriden for getting the product from a purchase order."""
        for inspection in self:
            super()._compute_product_id()
            if inspection.object_id and inspection.object_id._name == "purchase.order":
                inspection.product_id = inspection.object_id.product_id

    def object_selection_values(self):
        objects = super().object_selection_values()
        objects.append(("purchase.order", "Purchase Order"))
        return objects

    purchase_id = fields.Many2one(
        comodel_name="purchase.order", compute="_compute_purchase_id", store=True
    )
