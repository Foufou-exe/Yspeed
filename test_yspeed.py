import unittest
from unittest.mock import patch, MagicMock
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from yspeed import yspeed

class TestYourClass(unittest.TestCase):
    def setUp(self):
        self.yspeed = yspeed()

    def test_best_serveur(self):
        # Mock the _extracted_from_get_speedtest_10 method to return a desired output
        with patch.object(self.yspeed, '_extracted_from_get_speedtest_10') as mock_extracted:
            mock_driver = MagicMock()
            mock_driver.find_element.side_effect = [
                MagicMock(text="Fournisseur Test"), MagicMock(text="Server Test")]
            mock_extracted.return_value = mock_driver
            result = self.yspeed.best_serveur()
            self.assertIsInstance(result, dict)
            self.assertIn("fournisseur", result)
            self.assertIn("Serveur", result)

    def test_get_ip_info(self):
        with patch('requests.get') as mock_get:
            mock_get.return_value.json.return_value = {
                'ip': '1.2.3.4',
                'city': 'Test City',
                'region': 'Test Region',
                'country': 'Test Country',
                'org': 'Test Operator'
            }
            result = self.yspeed.get_ip_info()
            self.assertIsInstance(result, dict)
            self.assertEqual(result["ip"], "1.2.3.4")
            self.assertEqual(result["city"], "Test City")
            self.assertEqual(result["region"], "Test Region")
            self.assertEqual(result["country"], "Test Country")
            self.assertEqual(result["operator"], "Test Operator")

if __name__ == '__main__':
    unittest.main()