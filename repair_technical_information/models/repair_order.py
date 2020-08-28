# Copyright 2020 - TODAY, Marcel Savegnago - Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class RepairOrder(models.Model):

    _inherit = 'repair.order'

    technical_information = fields.Html('Technical Information')
