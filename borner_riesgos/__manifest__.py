{
    'name': 'Riesgos Borner',
    'version': '18.0.1.0.0',
    'summary': 'Modulo de prueba tecnica para Borner',
    'description': """
    Modulo de prueba tecnica para Borner:
    
    Características:
    - Se crea el modelo de riesgos
    - Se crean las vistas formulario y lista
    - Se crea accion 
    """,

    'author': 'Andres Pineda',
    'website': 'https://github.com/APinedaT',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/borner_risks.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}