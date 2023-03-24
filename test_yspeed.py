"""
Test file for the yspeed.py file
"""
import unittest
from unittest.mock import Mock, patch, MagicMock
from contextlib import contextmanager
from yspeed import Yspeed, gather_network_info, print_network_info, clear_screen

@contextmanager
def progress_context_manager():
    """
    Context manager for the progress bar
    """
    progress_mock = MagicMock()
    progress_mock.__enter__.return_value = progress_mock
    yield progress_mock
    progress_mock.__exit__.assert_called_once()
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
            
    def test_gather_network_info(self):
        """
        Test the gather_network_info method
        """
        # Mock Yspeed to return test data
        speedtest_mock = Mock()
        speedtest_mock.get_ip_info.return_value = {"ip": "1.2.3.4"}
        speedtest_mock.best_serveur.return_value = {"Serveur": "Test Server"}
        speedtest_mock.get_speedtest.return_value = {"download": "100 Mbps"}

        with progress_context_manager() as progress_mock:
            result = gather_network_info(speedtest_mock, progress_mock)

        self.assertIn("ip", result)
        self.assertIn("Serveur", result)
        self.assertIn("download", result)

    def test_print_network_info(self):
        """
        Test the print_network_info method
        """
        # Mock Console to capture printed output
        console_mock = Mock()

        info = {
            "operator": "Test Operator",
            "ip": "1.2.3.4",
            "city": "Test City",
            "region": "Test Region",
            "country": "Test Country",
            "fournisseur": "Test Fournisseur",
            "Serveur": "Test Server",
            "download": "100 Mbps",
            "upload": "50 Mbps",
            "ping": "10 ms"
        }

        print_network_info(console_mock, info)

        console_mock.print.assert_any_call("Operator: [bold green]Test Operator[/bold green]", style="blue", justify="center")
        console_mock.print.assert_any_call("IP: [bold green]1.2.3.4[/bold green]", style="blue", justify="center")
        console_mock.print.assert_any_call("Server: [bold green]Test Server[/bold green]", style="blue", justify="center")
        console_mock.print.assert_any_call("Download: [bold green]100 Mbps[/bold green]", style="blue", justify="center")
        console_mock.print.assert_any_call("Upload: [bold green]50 Mbps[/bold green]", style="blue", justify="center")
        console_mock.print.assert_any_call("Ping: [bold green]10 ms[/bold green]", style="blue", justify="center")
        console_mock.print.assert_any_call("City: [bold green]Test City[/bold green]", style="blue", justify="center")
        console_mock.print.assert_any_call("Region: [bold green]Test Region[/bold green]", style="blue", justify="center")
        console_mock.print.assert_any_call("Country: [bold green]Test Country[/bold green]", style="blue", justify="center")
        console_mock.print.assert_any_call("Fournisseur: [bold green]Test Fournisseur[/bold green]", style="blue", justify="center")

if __name__ == '__main__':
    unittest.main()
