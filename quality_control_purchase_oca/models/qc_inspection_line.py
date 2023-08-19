# Copyright 2023 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class QcInspectionLine(models.Model):

    _inherit = "qc.inspection.line"

    purchase_id = fields.Many2one(
        comodel_name="purchase.order",
        related="inspection_id.purchase_id",
        store=True,
        string="Purchase order",
    )
