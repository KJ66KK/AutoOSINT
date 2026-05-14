import unittest
from core.models import ModuleResult
from modules.email.breach_check import EmailBreachModule

class TestEmailBreachModule(unittest.TestCase):
    def setUp(self):
        self.module = EmailBreachModule()

    def test_scan_returns_valid_model(self):
        result = self.module.scan("test@example.com")
        self.assertIsInstance(result, ModuleResult)
        self.assertTrue(result.success)
        self.assertEqual(result.module_name, "BreachCheck")
        self.assertIn("breaches_found", result.data)

if __name__ == '__main__':
    unittest.main()
