{
    'name': 'Research Management',
    'version': '15.0.1.0.0',
    'sequence': 100,
    'depends': ['base',
                'contacts',
                'product',
                'stock',
                'sale',
                'account',
                'website',
                ],
    'assets': {
        'web.assets_backend': [
            'research_management/static/src/js/action_manager.js'],
    },

    'data': [
        'security/ir.model.access.csv',
        'view/research_view.xml',
        'data/sequence.xml',
        'data/scholar_sequence.xml',
        'data/smart_button.xml',
        'security/security_group.xml',
        'wizard/wizard.xml',
        'report/report.xml',
    ],
    'license': 'LGPL-3',
}
