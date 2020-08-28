# Copyright 2020 - TODAY, Escodoo
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Repair Timeline View',
    'summary': """
        Add timeline view""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Escodoo,Odoo Community Association (OCA)',
    'website': 'https://github.com/oca/manufacture',
    'depends': [
        'repair_calendar_view',
        'web_timeline',
    ],
    'data': [
        'views/repair_order.xml',
    ],
    'demo': [
    ],
}
