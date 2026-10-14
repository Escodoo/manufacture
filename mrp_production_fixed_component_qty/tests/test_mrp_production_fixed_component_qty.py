# Copyright 2026 - TODAY, Cristiano Mafra Junior <cristiano.mafra@escodoo.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestMrpProductionFixedComponentQty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.component = cls.env["product.product"].create(
            {"name": "Component", "is_storable": True}
        )
        cls.manual_component = cls.env["product.product"].create(
            {"name": "Manual Component", "is_storable": True}
        )
        cls.finished = cls.env["product.product"].create(
            {"name": "Finished", "is_storable": True}
        )
        cls.bom = cls.env["mrp.bom"].create(
            {
                "product_id": cls.finished.id,
                "product_tmpl_id": cls.finished.product_tmpl_id.id,
                "product_qty": 1.0,
                "type": "normal",
            }
        )
        cls.env["mrp.bom.line"].create(
            {
                "bom_id": cls.bom.id,
                "product_id": cls.component.id,
                "product_qty": 2.0,
            }
        )
        stock_location = cls.env.ref("stock.stock_location_stock")
        for product in (cls.component, cls.manual_component):
            cls.env["stock.quant"]._update_available_quantity(
                product, stock_location, 100
            )

    def _create_mo(self, qty=1.0, manual_component_qty=None):
        mo = self.env["mrp.production"].create(
            {
                "product_id": self.finished.id,
                "product_qty": qty,
                "bom_id": self.bom.id,
            }
        )
        mo.action_confirm()
        if manual_component_qty is not None:
            mo.write(
                {
                    "move_raw_ids": [
                        (
                            0,
                            0,
                            {
                                "name": self.manual_component.display_name,
                                "product_id": self.manual_component.id,
                                "product_uom_qty": manual_component_qty,
                                "product_uom": self.manual_component.uom_id.id,
                                "location_id": mo.location_src_id.id,
                                "location_dest_id": mo.production_location_id.id,
                            },
                        )
                    ]
                }
            )
        return mo

    def _change_qty(self, mo, new_qty):
        wizard = self.env["change.production.qty"].create(
            {"mo_id": mo.id, "product_qty": new_qty}
        )
        wizard.change_prod_qty()

    def _move_for(self, mo, product):
        return mo.move_raw_ids.filtered(lambda m: m.product_id == product)

    def test_manual_component_defaults_to_fixed(self):
        mo = self._create_mo(manual_component_qty=3)
        move = self._move_for(mo, self.manual_component)
        self.assertTrue(move.fixed_qty)

    def test_bom_component_defaults_to_not_fixed(self):
        mo = self._create_mo()
        move = self._move_for(mo, self.component)
        self.assertFalse(move.fixed_qty)

    def test_fixed_component_is_not_rescaled_on_qty_change(self):
        mo = self._create_mo(manual_component_qty=3)
        self._change_qty(mo, 4)
        move = self._move_for(mo, self.manual_component)
        self.assertEqual(move.product_uom_qty, 3)

    def test_bom_component_is_still_rescaled_on_qty_change(self):
        mo = self._create_mo(manual_component_qty=3)
        self._change_qty(mo, 4)
        move = self._move_for(mo, self.component)
        self.assertEqual(move.product_uom_qty, 8)

    def test_unchecking_fixed_qty_allows_rescale(self):
        mo = self._create_mo(manual_component_qty=3)
        move = self._move_for(mo, self.manual_component)
        move.fixed_qty = False
        self._change_qty(mo, 4)
        self.assertEqual(move.product_uom_qty, 12)

    def test_update_info_excludes_fixed_moves(self):
        """Regression: the change-log message the wizard posts must not
        claim a fixed move's quantity changed when it was, in fact,
        restored to its original value.
        """
        mo = self._create_mo(manual_component_qty=3)
        fixed_move = self._move_for(mo, self.manual_component)
        update_info = mo._update_raw_moves(4 / 1.0)
        self.assertNotIn(fixed_move, [info[0] for info in update_info])
