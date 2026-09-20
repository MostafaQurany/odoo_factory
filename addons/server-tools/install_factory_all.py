import sys
import odoo
from odoo import api, SUPERUSER_ID

def main():
    print("Initializing Odoo environment...")
    odoo.tools.config.parse_config([
        '-d', 'odoo',
        '--db_host=db',
        '-r', 'odoo',
        '-w', 'odoo',
        '--addons-path=/mnt/extra-addons/manufacture,/mnt/extra-addons/ddmrp,/mnt/extra-addons/stock-logistics-warehouse,/mnt/extra-addons/stock-logistics-orderpoint,/mnt/extra-addons/server-backend,/mnt/extra-addons/server-tools,/mnt/extra-addons/stock-logistics-workflow,/mnt/extra-addons/web,/mnt/extra-addons/stock-logistics-availability,/mnt/extra-addons/queue,/usr/lib/python3/dist-packages/odoo/addons'
    ])

    registry = odoo.registry('odoo')
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        Module = env['ir.module.module']

        print("Updating module list from disk...")
        Module.update_list()

        targets = ['odoo_factory_all', 'clothing_factory_demo']
        mods = Module.search([('name', 'in', targets)])
        print("Target modules status:", [(m.name, m.state) for m in mods])

        print("Starting immediate installation of target modules...")
        mods.button_immediate_install()
        cr.commit()
        print("ALL TARGET MODULES AND DEPENDENCIES INSTALLED SUCCESSFULLY!")

if __name__ == '__main__':
    main()
