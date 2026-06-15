{
    "name": "Balance de Comprobacion por Terceros CO",
    "summary": "Reporte de balance de comprobacion por terceros para contabilidad colombiana",
    "version": "18.0.1.0.0",
    "category": "Accounting",
    "license": "LGPL-3",
    "author": "Andres Pineda",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "wizard/balance_comprobacion_terceros_wizard_views.xml",
        "report/balance_comprobacion_terceros_actions.xml",
        "report/balance_comprobacion_terceros_templates.xml",
        "views/menu.xml"
    ],
    "installable": True,
    "application": False
}
