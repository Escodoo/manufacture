# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    def _update_raw_moves(self, factor):
        """Exclude moves flagged ``fixed_qty`` from the proportional rescale
        core applies here when the quantity to produce changes on an
        already confirmed MO.

        Core itself offers no hook to skip individual moves, so this calls
        `super()` first (letting it rescale everything as usual) and then
        restores the pre-rescale quantity on the moves that should have
        been left alone, removing them from the returned `update_info` so
        the change-log message posted by the wizard doesn't report a
        change that was, in fact, reverted.
        """
        self.ensure_one()
        fixed_moves = self.move_raw_ids.filtered(
            lambda m: m.state not in ("done", "cancel") and m.fixed_qty
        )
        original_qty = {move.id: move.product_uom_qty for move in fixed_moves}
        update_info = super()._update_raw_moves(factor)
        for move, _old_qty, _new_qty in update_info:
            if move.id in original_qty:
                move.product_uom_qty = original_qty[move.id]
        return [info for info in update_info if info[0].id not in original_qty]
