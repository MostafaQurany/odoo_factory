import unittest
import os
import sys

# Add project root to sys.path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.factory.scan_modules import parse_manifest_ast, scan_all_modules
from scripts.factory.build_graph import detect_cycles, build_dependency_graph

class TestModuleScanner(unittest.TestCase):
    def test_parse_manifest_ast_valid(self):
        sample_code = """{
            'name': 'Sample Module',
            'version': '18.0.1.0.0',
            'category': 'Manufacturing',
            'depends': ['base', 'mrp'],
            'installable': True,
            'application': False,
            'license': 'LGPL-3',
        }"""
        data = parse_manifest_ast(sample_code)
        self.assertEqual(data.get('name'), 'Sample Module')
        self.assertEqual(data.get('version'), '18.0.1.0.0')
        self.assertEqual(data.get('depends'), ['base', 'mrp'])
        self.assertTrue(data.get('installable'))
        self.assertEqual(data.get('license'), 'LGPL-3')

    def test_cycle_detection_no_cycle(self):
        graph = {
            'A': ['B', 'C'],
            'B': ['C'],
            'C': []
        }
        cycles = detect_cycles(graph)
        self.assertEqual(len(cycles), 0)

    def test_cycle_detection_with_cycle(self):
        graph = {
            'A': ['B'],
            'B': ['C'],
            'C': ['A']
        }
        cycles = detect_cycles(graph)
        self.assertTrue(len(cycles) > 0)
        # Cycle should contain A, B, C
        flat_nodes = set([item for sub in cycles for item in sub])
        self.assertTrue({'A', 'B', 'C'}.issubset(flat_nodes))

if __name__ == '__main__':
    unittest.main()
