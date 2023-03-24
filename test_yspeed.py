"""
Test file for the yspeed.py file
"""
import unittest
from unittest.mock import patch, MagicMock
from yspeed import Yspeed

class TestYourClass(unittest.TestCase):
    """ 
    Test class for the Yspeed class
    """
    def setUp(self):
        """ 
        Setup the test class
        """
        self.yspeed = Yspeed()

    def test_best_serveur(self):
        """
        Test the best_serveur method
        """
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
        """
        Test the get_ip_info method
        """
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