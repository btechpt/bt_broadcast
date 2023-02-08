# -*- coding: utf-8 -*-
{
    'name': "Broadcast",

    'summary': """
        Broadcast messages to all devices
        """,

    'description': """
        Broadcast messages to all devices
    """,

    'author': "Btech Techonology",
    'website': "https://btech.id",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Btech/Broadcast',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'hr'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        "security/security.xml",
        "security/ir.model.access.csv",
        'views/assets.xml',
        'views/views.xml',
        'views/templates.xml',
        'data/mail_template_standalone.xml',
        'data/data_setting.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'qweb': [
        'static/src/xml/broadcast.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'GPL-3',
    'images': ['static/description/images/main_screenshot.png']
}
