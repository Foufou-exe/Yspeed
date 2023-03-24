"""Docstring for module Yspeed.
"""

import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Yspeed:
    """
    A class that provides methods to retrieve information about the user's,
    Internet connection speed and IP address.
    Methods:
    best_serveur():
    Retrieves and returns detailed IP address
    information using the https://www.speedtest.net/ service.
    Information retrieved includes:
    Provider: the name of the user's Internet Service Provider,
    obtained using Selenium.
    Server: the name of the server used for the connection,
    also obtained using Selenium.
    This method uses the 'requests' library to make an HTTP request and
    the 'selenium' library to interact with
    a web browser to obtain additional information,
    including the provider name and server name.
    get_ip_info():
    Retrieves information about the user's public IP address,
    such as city, region, country, and operator.
    This function makes a request to the ipinfo.io
    service to get information about the user's public IP address.
    The information retrieved includes IP address,
    city, region, country, and operator.
    Returns:
    dict: A dictionary containing information about
    the user's public IP address.
    get_speedtest():
    Retrieves and returns the results of an Internet
    connection speed test using the online service Speedtest.
    The information retrieved includes:
    Download Speed: The speed at which data is downloaded from 
    the Internet to the user's computer.
    Upload speed: the speed at which data is sent
    from the user's computer to the Internet.
    Ping: the latency of the connection, measured in milliseconds.
    This method uses the 'selenium' library to interact
    with a web browser and automate the speed test on the Speedtest site.
    It waits for the test to finish, extracts the results and
    closes the browser before returning the data.
    _extracted_from_get_speedtest_10():
    A private method that initializes a web browser using Selenium and
    loads the Speedtest site (https://www.speedtest.net/).
    This method is used by the 'ipinfo' and 'speedtest' methods
    to automate interactions with the web site.
    get_webdriver(browser):
    This method is used to initialize and return an instance of
    Selenium webdriver based on the browser specified in argument.
    It supports Chrome, Firefox and Edge browsers.
    """
    def best_serveur(self):
        """
        Retrieves and returns detailed IP address information
        using the https://www.speedtest.net/ service.
        Information retrieved includes:
        Provider: the name of the user's Internet Service Provider,
        obtained using Selenium.
        Server: the name of the server used for the connection,
        also obtained using Selenium.
        This method uses the 'requests' library to make an HTTP request
        and the 'selenium' library to interact with
        a web browser to obtain additional information,
        including the provider name and server name.
        """
        driver = self._extracted_from_get_speedtest_10()
        fournisseur = driver.find_element(By.CLASS_NAME, 'hostUrl').text
        server = driver.find_element(By.CLASS_NAME, 'name').text
        driver.quit()
        return {"fournisseur": fournisseur, "Serveur": server}
    def get_ip_info(self):
        """
        Retrieves information about the user's public IP address,
        such as city, region, country, and operator.
        This function makes a request to the ipinfo.io service 
        to get information about the user's public IP address.
        The information retrieved includes IP address,
        city, region, country, and operator.
        Returns:
        dict: A dictionary containing information about the user's public IP address.
        """
        response = requests.get("http://ipinfo.io/json", timeout=5)
        data = response.json()
        ip_public = data['ip']
        city = data['city']
        region = data['region']
        country = data['country']
        operator = data['org']
        return {"ip":ip_public,"city":city,"region":region,"country":country,"operator":operator}
    def get_speedtest(self):
        """
        Retrieves and returns the results of 
        an Internet connection speed test using the online service Speedtest.
        The information retrieved includes:
        Download Speed: The speed at which data is
        downloaded from the Internet to the user's computer.
        Upload speed: the speed at which 
        data is sent from the user's computer to the Internet.
        Ping: the latency of the connection, measured in milliseconds.
        This method uses the 'selenium' library to interact with a web browser and
        automate the speed test on the Speedtest site. It waits for the test to finish,
        extracts the results and closes the browser before returning the data.
        """
        driver = self._extracted_from_get_speedtest_10()
        go_button = driver.find_element(By.CSS_SELECTOR, '.start-button a')
        go_button.click()
        time.sleep(45)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'result-data-large.number.result-data-value.download-speed')
        ))
        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'result-data-large.number.result-data-value.upload-speed')))
        wait.until(EC.visibility_of_element_located(
            (By.CLASS_NAME, 'result-data-value.ping-speed')))
        download_speed = driver.find_element(
            By.CLASS_NAME, 'result-data-large.number.result-data-value.download-speed').text
        upload_speed = driver.find_element(
            By.CLASS_NAME, 'result-data-large.number.result-data-value.upload-speed').text
        ping_speed = driver.find_element(
            By.CLASS_NAME, 'result-data-value.ping-speed').text
        driver.quit()
        return {"download": download_speed, "upload": upload_speed, "ping": ping_speed, }
    def _extracted_from_get_speedtest_10(self):
        result = self._extracted_from_speedtest_10()
        go_button = result.find_element(By.ID,'onetrust-accept-btn-handler')
        go_button.click()
        return result
    def _extracted_from_speedtest_10(self):
        """
        This private method (_extracted_from_speedtest_10) initializes
        a web browser using Selenium and loads the Speedtest site(https://www.speedtest.net/).
        This method is used by the 'ipinfo' and 'speedtest'
        methods to automate interactions with the web site.
        The main steps of this method are as follows:
        Retrieve the browser name from the command line arguments,
        if available, otherwise use Chrome by default.
        Get the instance of the webdriver corresponding 
        to the chosen browser by calling the get_webdriver method.
        Load the Speedtest site (https://www.speedtest.net/) using the webdriver.
        Wait 5 seconds to allow the site to load correctly.
        The method returns the instance of the webdriver initialized and
        ready to interact with the Speedtest site.
        """
        browser = sys.argv[1] if len(sys.argv) > 1 else "chrome"
        result = self.get_webdriver(browser)
        result.get("https://www.speedtest.net/")
        time.sleep(5)
        return result
    def get_webdriver(self, browser):
        """
        This method (get_webdriver) is used to initialize and
        return an instance of Selenium webdriver based
        on the browser specified in argument.
        It supports Chrome, Firefox and Edge browsers
        The main steps of this method are as follows:
        Check which browser has been specified as an argument.
        Configure the webdriver options for the chosen browser,
        including enabling headless mode and
        disabling some console message levels.
        Return the instance of the webdriver configured for
        the chosen browser.
        If the browser specified in the argument is not supported,
        the method will throw a ValueError exception.    
        """
        if browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--log-level=3")
            options.add_experimental_option(
                'excludeSwitches', ['enable-logging'])
            return webdriver.Chrome(options=options)
        if browser.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.log.level = "fatal"
            return webdriver.Firefox(options=options)
        if browser.lower() == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("--headless")
            options.add_argument("--log-level=3")
            return webdriver.Edge(options=options)
        raise ValueError("Browser not supported")
if __name__ == '__main__':
    speedtest = Yspeed()
    print(speedtest.get_ip_info())
    print(speedtest.get_speedtest())
    print(speedtest.best_serveur())
