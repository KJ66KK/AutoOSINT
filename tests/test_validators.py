import unittest
from utils.validators import is_valid_email, is_valid_domain, is_valid_phone, determine_target_type

class TestValidators(unittest.TestCase):
    def test_valid_email(self):
        self.assertTrue(is_valid_email("test@example.com"))
        self.assertTrue(is_valid_email("first.last+tag@domain.co.uk"))
        self.assertFalse(is_valid_email("not-an-email"))
        self.assertFalse(is_valid_email("test@example"))

    def test_valid_domain(self):
        self.assertTrue(is_valid_domain("example.com"))
        self.assertTrue(is_valid_domain("sub.example.co.uk"))
        self.assertFalse(is_valid_domain("http://example.com"))
        self.assertFalse(is_valid_domain("example"))

    def test_valid_phone(self):
        self.assertTrue(is_valid_phone("+14155552671"))
        self.assertTrue(is_valid_phone("14155552671"))
        self.assertTrue(is_valid_phone("(415) 555-2671"))
        self.assertFalse(is_valid_phone("not a number"))

    def test_determine_target_type(self):
        self.assertEqual(determine_target_type("admin@nasa.gov"), "email")
        self.assertEqual(determine_target_type("google.com"), "domain")
        self.assertEqual(determine_target_type("+14155552671"), "phone")
        self.assertEqual(determine_target_type("cyber_king"), "username")

if __name__ == '__main__':
    unittest.main()
