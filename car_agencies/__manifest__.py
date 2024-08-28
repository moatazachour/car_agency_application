{
    'name': 'Car Agency Management',
    'author': 'Moataz',
    'website': 'www.moatazagency.tech',
    'summary': 'Manage car agencies',
    'depends': ['base','mail'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/car_damage_wizard.xml',
        'views/car_brand.xml',
        'views/car.xml',
        'views/maintenance.xml',
        'views/agency.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
}
