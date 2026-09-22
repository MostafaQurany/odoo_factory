import unittest
import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from scripts.ci_gate import check_graph_cycles, check_profile_safety

class TestCIGate(unittest.TestCase):
    def test_ci_checks(self):
        self.assertTrue(check_graph_cycles())
        self.assertTrue(check_profile_safety())

if __name__ == '__main__':
    unittest.main()
