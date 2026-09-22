# -*- coding: utf-8 -*-
import sys
import odoo
from odoo import api, fields, SUPERUSER_ID

def run():
    print("[*] Initializing Odoo Environment...")
    odoo.tools.config.parse_config(['-c', '/etc/odoo/odoo.conf', '-d', 'factory_dev'])
    
    registry = odoo.registry('factory_dev')
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        # 1. Company & Localization
        print("[1/8] Updating Factory Company Profile...")
        company = env.ref('base.main_company')
        egypt = env.ref('base.eg', raise_if_not_found=False)
        egp = env.ref('base.EGP', raise_if_not_found=False)
        
        company_vals = {
            'name': 'Alexandria Industrial & Manufacturing Co. (AIMC)',
            'street': 'Plot 14, Sector 3, Borg El Arab Industrial Zone',
            'city': 'Alexandria',
            'phone': '+20 3 459 8800',
            'email': 'operations@aimc-factory.eg',
            'website': 'https://www.aimc-factory.eg',
            'vat': 'EG-984729184',
            'factory_po_approval_limit': 25000.0,
            'factory_enable_egp_localization': True,
        }
        if egypt:
            company_vals['country_id'] = egypt.id
        company.write(company_vals)

        # 2. Warehouse & 10 Factory Locations
        print("[2/8] Initializing 10 Industrial Warehouse Locations...")
        warehouse = env['stock.warehouse'].search([('company_id', '=', company.id)], limit=1)
        if not warehouse:
            warehouse = env['stock.warehouse'].create({
                'name': 'Borg El Arab Main Factory Warehouse',
                'code': 'WH-BEA',
                'company_id': company.id,
            })
        else:
            warehouse.write({'name': 'Borg El Arab Main Factory Warehouse', 'code': 'WH-BEA'})
        
        warehouse.action_create_factory_locations()

        loc_rm = warehouse.loc_raw_materials_id
        loc_wip = warehouse.loc_wip_id
        loc_fg = warehouse.loc_finished_goods_id
        loc_qc = warehouse.loc_quality_hold_id
        loc_scrap = warehouse.loc_scrap_id

        # 3. Products Master
        print("[3/8] Fetching Products & Partners...")
        p_rm_001 = env['product.product'].search([('default_code', '=', 'RM-001')], limit=1)
        p_rm_002 = env['product.product'].search([('default_code', '=', 'RM-002')], limit=1)
        p_rm_003 = env['product.product'].search([('default_code', '=', 'RM-003')], limit=1)
        p_pkg_001 = env['product.product'].search([('default_code', '=', 'PKG-001')], limit=1)
        p_comp_001 = env['product.product'].search([('default_code', '=', 'COMP-001')], limit=1)
        p_fg_001 = env['product.product'].search([('default_code', '=', 'FG-001')], limit=1)


        for p in [p_rm_001, p_rm_002, p_rm_003, p_pkg_001, p_comp_001, p_fg_001]:
            if p:
                p.product_tmpl_id.is_storable = True

        vendor_steel = env['res.partner'].search([('name', '=', 'Apex Industrial Metals LLC')], limit=1)
        vendor_fasteners = env['res.partner'].search([('name', '=', 'Delta Precision Fasteners & Seals')], limit=1)
        customer_oem = env['res.partner'].search([('name', '=', 'Nile Machinery Manufacturing Corp')], limit=1)
        customer_dist = env['res.partner'].search([('name', '=', 'Middle East Industrial Supplies & Spares')], limit=1)

        # 4. Stock on Hand (Stock Quants)
        print("[4/8] Populating Physical Stock on Hand...")
        Quant = env['stock.quant']
        stock_allocations = [
            (p_rm_001, loc_rm, 650.0),
            (p_rm_002, loc_rm, 8000.0),
            (p_rm_003, loc_rm, 350.0),
            (p_pkg_001, loc_rm, 400.0),
            (p_comp_001, loc_wip, 75.0),
            (p_fg_001, loc_fg, 40.0),
            (p_rm_001, loc_qc, 25.0),
            (p_rm_001, loc_scrap, 5.0),
        ]

        for product, location, qty in stock_allocations:
            if product and location:
                quant = Quant.search([
                    ('product_id', '=', product.id),
                    ('location_id', '=', location.id),
                ], limit=1)
                if quant:
                    quant.inventory_quantity = qty
                    quant.action_apply_inventory()
                else:
                    quant = Quant.create({
                        'product_id': product.id,
                        'location_id': location.id,
                        'inventory_quantity': qty,
                    })
                    quant.action_apply_inventory()

        # 5. Purchase Orders
        print("[5/8] Creating Realistic Purchase Orders...")
        PO = env['purchase.order']
        
        if vendor_steel and p_rm_001:
            po1 = PO.create({
                'partner_id': vendor_steel.id,
                'company_id': company.id,
                'order_line': [(0, 0, {
                    'product_id': p_rm_001.id,
                    'product_qty': 150.0,
                    'price_unit': 45.0,
                    'date_planned': fields.Datetime.now(),
                })]
            })
            po1.button_confirm()
            for picking in po1.picking_ids:
                for move in picking.move_ids:
                    move.quantity = move.product_uom_qty
                    move.picked = True
                try:
                    picking.button_validate()
                except Exception:
                    pass

        if vendor_fasteners and p_rm_002:
            po2 = PO.create({
                'partner_id': vendor_fasteners.id,
                'company_id': company.id,
                'order_line': [(0, 0, {
                    'product_id': p_rm_002.id,
                    'product_qty': 2500.0,
                    'price_unit': 1.5,
                    'date_planned': fields.Datetime.now(),
                })]
            })
            po2.button_confirm()

        if vendor_steel and p_rm_001:
            po3 = PO.create({
                'partner_id': vendor_steel.id,
                'company_id': company.id,
                'order_line': [(0, 0, {
                    'product_id': p_rm_001.id,
                    'product_qty': 800.0,
                    'price_unit': 45.0,
                    'date_planned': fields.Datetime.now(),
                })]
            })
            try:
                po3.button_confirm()
            except Exception:
                pass

        # 6. Sales Orders
        print("[6/8] Creating Industrial Sales Orders...")
        SO = env['sale.order']

        if customer_oem and p_fg_001:
            so1 = SO.create({
                'partner_id': customer_oem.id,
                'company_id': company.id,
                'factory_demand_type': 'make_to_order',
                'order_line': [(0, 0, {
                    'product_id': p_fg_001.id,
                    'product_uom_qty': 12.0,
                    'price_unit': 350.0,
                })]
            })
            so1.action_confirm()

        if customer_dist and p_fg_001:
            so2 = SO.create({
                'partner_id': customer_dist.id,
                'company_id': company.id,
                'factory_demand_type': 'make_to_stock',
                'order_line': [(0, 0, {
                    'product_id': p_fg_001.id,
                    'product_uom_qty': 8.0,
                    'price_unit': 340.0,
                })]
            })
            so2.action_confirm()
            for pick in so2.picking_ids:
                for move in pick.move_ids:
                    move.quantity = move.product_uom_qty
                    move.picked = True
                try:
                    pick.button_validate()
                except Exception:
                    pass

        if customer_oem and p_fg_001:
            SO.create({
                'partner_id': customer_oem.id,
                'company_id': company.id,
                'factory_demand_type': 'make_to_order',
                'state': 'sent',
                'order_line': [(0, 0, {
                    'product_id': p_fg_001.id,
                    'product_uom_qty': 50.0,
                    'price_unit': 325.0,
                })]
            })

        # 7. Manufacturing Orders (MOs)
        print("[7/8] Generating Live Manufacturing Orders...")
        MO = env['mrp.production']
        bom_fg = env['mrp.bom'].search([('code', '=', 'BOM-FG-001-REV1')], limit=1)
        bom_comp = env['mrp.bom'].search([('code', '=', 'BOM-COMP-001-REV1')], limit=1)

        if bom_fg and p_fg_001:
            mo1 = MO.create({
                'product_id': p_fg_001.id,
                'product_uom_id': p_fg_001.uom_id.id,
                'product_qty': 10.0,
                'bom_id': bom_fg.id,
                'company_id': company.id,
            })
            mo1.action_confirm()
            mo1.action_assign()

        if bom_comp and p_comp_001:
            mo2 = MO.create({
                'product_id': p_comp_001.id,
                'product_uom_id': p_comp_001.uom_id.id,
                'product_qty': 25.0,
                'bom_id': bom_comp.id,
                'company_id': company.id,
            })
            mo2.action_confirm()
            mo2.action_assign()

        if bom_fg and p_fg_001:
            mo3 = MO.create({
                'product_id': p_fg_001.id,
                'product_uom_id': p_fg_001.uom_id.id,
                'product_qty': 30.0,
                'bom_id': bom_fg.id,
                'company_id': company.id,
            })
            mo3.action_confirm()

        # 8. Maintenance Equipment & Service Requests
        print("[8/8] Creating Equipment Assets & Maintenance Workflows...")
        Equip = env['factory.equipment']
        Req = env['factory.maintenance.request']
        
        wc_cut = env['mrp.workcenter'].search([('code', '=', 'WC-CUT')], limit=1)
        wc_weld = env['mrp.workcenter'].search([('code', '=', 'WC-WELD')], limit=1)
        wc_assy = env['mrp.workcenter'].search([('code', '=', 'WC-ASSY')], limit=1)

        eq1 = Equip.create({
            'name': 'TRUMPF TruLaser 3030 Fiber Laser Table',
            'code': 'EQ-LASER-01',
            'workcenter_id': wc_cut.id if wc_cut else False,
            'model_number': 'TruLaser 3030',
            'serial_number': 'TRU-3030-2023-089',
            'state': 'operational',
        })

        eq2 = Equip.create({
            'name': 'Miller Dynasty 400 TIG/MIG Welding Cell',
            'code': 'EQ-WELD-02',
            'workcenter_id': wc_weld.id if wc_weld else False,
            'model_number': 'Dynasty 400',
            'serial_number': 'MIL-DYN-400-EG',
            'state': 'operational',
        })

        eq3 = Equip.create({
            'name': 'Haas VF-4 4-Axis CNC Machining Center',
            'code': 'EQ-CNC-03',
            'workcenter_id': wc_assy.id if wc_assy else False,
            'model_number': 'VF-4',
            'serial_number': 'HAA-VF4-99120',
            'state': 'operational',
        })

        Req.create({
            'name': 'REQ-PM-001 Monthly Optical Alignment & Lens Cleaning',
            'equipment_id': eq1.id,
            'maintenance_type': 'preventive',
            'state': 'draft',
            'work_summary': 'Clean focus lenses, inspect nitrogen assist gas regulator and chiller temp.',
        })

        Req.create({
            'name': 'REQ-EM-002 Cooling System Temperature Sensor Replacement',
            'equipment_id': eq2.id,
            'maintenance_type': 'corrective',
            'failure_reason': 'sensor',
            'state': 'in_progress',
            'downtime_hours': 2.5,
            'work_summary': 'Overheating alarm on secondary circuit. Replacing thermistor.',
        })
        if wc_weld:
            wc_weld.write({'working_state': 'blocked'})

        # Commit Transaction
        cr.commit()
        print("[SUCCESS] All Factory ERP mock data successfully populated in factory_dev!")

if __name__ == '__main__':
    run()
