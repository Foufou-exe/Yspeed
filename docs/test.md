# Test

### Unit tests for Yspeed

```python linenums="1"
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

    @patch('yspeed.Halo')
    @patch('yspeed.time.sleep', MagicMock(return_value=None))
    def test_run_speedtest(self, mock_halo):
        """ Test the run_speedtest method"""
        # Replace 'YourClass' with the actual name of the class containing the `run_speedtest` function
        speedtest_obj = Yspeed()

        # Mock the get_speedtest method to return a predefined dictionary
        mock_speedtest = {'download': '100 Mbps', 'upload': '50 Mbps', 'ping': '20 ms'}
        speedtest_obj.get_speedtest = MagicMock(return_value=mock_speedtest)

        # Call the run_speedtest function and get the results
        result = speedtest_obj.run_speedtest()

        # Assert that the result is as expected
        self.assertEqual(result, mock_speedtest)

        # Assert that the Halo spinner is called with the expected parameters
        mock_halo.assert_called_with(spinner={'interval': 100, 'frames': ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']}, text="Démarrage du Speedtest", color="red", text_color="yellow")

    
    def setUp(self):
        """ 
        Setup the test class
        """
        self.yspeed = Yspeed()


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

```

The purpose of this test file is to test the various features of the Python library "yspeed". It uses the Python module "unittest" to perform the tests.

The file also imports other libraries such as "mock" and "patch" to simulate the inputs and outputs of certain functions and "contextmanager" to manage contexts.

The "TestYourClass" class inherits from "unittest.TestCase" and defines different tests for the "yspeed" functions. Each test method will start with "test_" and check the expected behaviour of a specific function using assertions.

The "setUp" method is executed before each test and allows the objects needed for the tests to be set up.

The test methods include "test_run_speedtest", "test_get_ip_info", "test_gather_network_info" and "test_print_network_info", which test the "run_speedtest", "get_ip_info", "gather_network_info" and "print_network_info" function respectively.

Finally, when this file is run as a main script, the "unittest.main()" method is called to run the tests. The results of the tests are displayed on the screen, indicating whether the tests passed or failed.