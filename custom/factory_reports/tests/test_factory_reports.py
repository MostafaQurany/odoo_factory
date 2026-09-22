# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestFactoryReports(TransactionCase):

    def test_01_verify_all_16_reports_registered(self):
        """Verify all 16 industrial production report actions exist in the registry."""
        report_xml_ids = [
            'factory_reports.action_report_mrp_order_card',
            'factory_reports.action_report_mrp_bom_sheet',
            'factory_reports.action_report_production_pick_list',
            'factory_reports.action_report_material_consumption',
            'factory_reports.action_report_finished_production',
            'factory_reports.action_report_stock_scrap',
            'factory_reports.action_report_rework_order',
            'factory_reports.action_report_qc_inspection',
            'factory_reports.action_report_lot_traceability',
            'factory_reports.action_report_stock_availability',
            'factory_reports.action_report_inventory_valuation',
            'factory_reports.action_report_purchase_incoming',
            'factory_reports.action_report_supplier_performance',
            'factory_reports.action_report_production_costing',
            'factory_reports.action_report_manufacturing_variance',
            'factory_reports.action_report_factory_delivery_slip',
        ]

        for xml_id in report_xml_ids:
            report = self.env.ref(xml_id, raise_if_not_found=False)
            self.assertTrue(report, f"Report action {xml_id} must be registered.")
            self.assertEqual(report.report_type, 'qweb-pdf')
