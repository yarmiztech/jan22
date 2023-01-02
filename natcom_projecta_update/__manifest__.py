# -*- coding: utf-8 -*-
{
    'name': "Natcom Projecta Edit",
    'author': 'Enzapps Private Limited',
    'company': 'Enzapps Private Limited',
    'maintainer': 'Enzapps Private Limited',
    'summary': """This module is for printing E-Invoice report for Zatca.""",

    'description': """This module is for printing E-Invoice report for Zatca.""",
    'website': "www.enzapps.com",
    'category': 'base',
    'version': '14.0',
    'images': ['static/description/icon.png'],
    'depends': ['base', 'account', 'sale', 'purchase', 'stock', 'arabic_strings', 'enz_ksa_phase_two_zatca','natcom_einvoice_formate','projecta_custom_formate'],
    'data': [
        'reports/header.xml',
        'reports/natcom_view.xml',
        'reports/natcom_view_without.xml',
        'reports/projecta_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
