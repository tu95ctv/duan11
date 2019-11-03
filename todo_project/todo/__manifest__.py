# -*- coding: utf-8 -*-
{
    'name': "todo",
    'summary': """Proficiency Test""",
    'description': """
        Proficiency Test
    """,
    'author': "Nguyen Duc Tu",
    'website': "",
    'category': 'Proficiency',
    'version': '0.1',
    'depends': ['base'],
    # always loaded
    'data': [
        'security/todo_security.xml',
        'data/todo_data.xml',
        'security/ir.model.access.csv',
        'views/todo_view.xml',
        'views/todo_menu.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
}