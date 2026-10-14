When the quantity to produce of an already confirmed Manufacturing Order is
changed (via the "Update Quantity" action), Odoo rescales the demand of
every open raw material move proportionally to the change -- including
components that were added by hand, with no Bill of Materials line behind
them, and were never meant to vary with the batch size (for example, a
fixed kit of consumables used once per job regardless of how many units
are produced).

Because this rescale works off whatever is currently stored rather than
recomputing from the Bill of Materials, and always rounds up, a handful of
quantity changes back and forth is enough to turn clean, whole-unit
demands into fractional, physically meaningless ones (for example "1.34"
units of an item that cannot be split).

This module adds a "Fixed Quantity" flag on each raw material move of a
Manufacturing Order. A flagged move is skipped by that rescale and keeps
whatever quantity was entered for it, no matter how many times the
quantity to produce changes afterwards.

Raw material moves added without a Bill of Materials line of their own are
flagged "Fixed Quantity" automatically when created, since there is no
recipe tying their quantity to the batch size in the first place. The flag
can still be checked or unchecked by hand on any component.
