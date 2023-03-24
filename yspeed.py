"""Docstring for module Yspeed.
"""

import sys
import time
import requests
import platform
import shutil
import os
from rich.console import Console
from rich.text import Text
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TextColumn
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
    
    
    def define_brower(self):
        system = platform.system().lower()
        
        if system == "windows":
            browser_executables = {
                "chrome": "chrome.exe",
                "firefox": "firefox.exe",
                "edge": "msedge.exe"
            }
            possible_paths = [
                os.path.join(os.environ["ProgramFiles"], "Google", "Chrome", "Application"),
                os.path.join(os.environ["ProgramFiles(x86)"], "Google", "Chrome", "Application"),
                os.path.join(os.environ["ProgramFiles"], "Mozilla Firefox"),
                os.path.join(os.environ["ProgramFiles(x86)"], "Mozilla Firefox"),
                os.path.join(os.environ["ProgramFiles"], "Microsoft", "Edge", "Application"),
                os.path.join(os.environ["ProgramFiles(x86)"], "Microsoft", "Edge", "Application"),
            ]
        elif system == "linux":
            browser_executables = {
                "chrome": "google-chrome",
                "firefox": "firefox",
                "edge": "microsoft-edge"
            }
            possible_paths = [
                "/usr/bin",
                "/usr/local/bin",
                "/opt/google/chrome",
                "/opt/microsoft/msedge",
            ]
        else:
            raise NotImplementedError(f"Platform '{system}' not supported")

        for path in possible_paths:
            for browser, executable in browser_executables.items():
                if os.path.isfile(os.path.join(path, executable)):
                    return browser

        return None
    
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
        
        result = self.get_webdriver(self.define_brower())
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

class TimeElapsedColumnWithLabel(TimeElapsedColumn):
    """A column that displays the time elapsed since the task started."""
    def render(self, task) -> Text:
        elapsed = task.finished_time if task.finished else task.elapsed
        return Text("Time: {:.1f}s".format(elapsed))
    
def gather_network_info(speedtest: Yspeed, progress: Progress) -> dict:
    """ This function (gather_network_info) gathers the network information"""
    with progress:
        task1 = progress.add_task("Getting IP info...",title="[cyan]Getting IP info...", total=1)
        info = speedtest.get_ip_info()
        progress.update(task1, advance=1)
        task2 = progress.add_task("Selecting best server...",title="[cyan]Selecting best server...", total=1)
        best = speedtest.best_serveur()
        progress.update(task2, advance=1)
        task3 = progress.add_task("Performing speedtest...",title="[cyan]Performing speedtest...", total=1)
        speed = speedtest.get_speedtest()
        progress.update(task3, advance=1)
        return {
            **info,
            **best,
            **speed,
        }
    
def print_network_info(console: Console, info: dict):
    """ 
    This function (print_network_info) prints the network information
    """
    clear_screen()
    console.print("Network Information", style="bold yellow", justify="center")
    console.print("Operator: [bold green]{operator}[/bold green]".format(**info), style="blue", justify="center")
    console.print("IP: [bold green]{ip}[/bold green]".format(**info), style="blue", justify="center")
    console.print("\nLocalisation", style="bold yellow", justify="center")
    console.print("City: [bold green]{city}[/bold green]".format(**info), style="blue", justify="center")
    console.print("Region: [bold green]{region}[/bold green]".format(**info), style="blue", justify="center")
    console.print("Country: [bold green]{country}[/bold green]".format(**info), style="blue", justify="center")
    console.print("\nBest Server", style="bold yellow", justify="center")
    console.print("Fournisseur: [bold green]{fournisseur}[/bold green]".format(**info), style="blue", justify="center")
    console.print("Server: [bold green]{Serveur}[/bold green]".format(**info), style="blue", justify="center")
    console.print("\nSpeedTest", style="bold yellow", justify="center")
    console.print("Download: [bold green]{download}[/bold green]".format(**info), style="blue", justify="center")
    console.print("Upload: [bold green]{upload}[/bold green]".format(**info), style="blue", justify="center")
    console.print("Ping: [bold green]{ping}[/bold green]".format(**info), style="blue", justify="center")

def author(console: Console):
    """
    This function (author) prints the author's name
    """
    version = "0.1.0"
    console.print("Author: Foufou-exe", style="grey35", justify="center")
    console.print("Github: https://github.com/Foufou-exe", style="grey35", justify="center")
    console.print(f"Version Yspeed: {version}", style="grey35", justify="center")

def clear_screen():
    """
        Efface l'écran
    """
    system_name = platform.system()
    if system_name == "Windows":
        # do something specific for Windows
        os.system('cls')
    elif system_name == "Linux":
        # do something specific for Linux
        os.system('clear')
    else:
        print(f"Le systeme ne supporte pas : {system_name}")
        
def main():
    """
    This function (main) is the main entry point of the script.
    """
    try:
        console = Console()
        speedtest = Yspeed()
        console.print("Welcome to Yspeed!", style="bold yellow", justify="center")
        author(console)
        
        console.print("\n\nGathering network information...", style="bold yellow", justify="center")
        with  Progress(TextColumn("{task.fields[title]}"),BarColumn(),TimeElapsedColumnWithLabel(),console=console) as progress:
            info = gather_network_info(speedtest, progress)
        print_network_info(console, info)
        console.print("\nGoodbye!", style="bold red", justify="center")
    except KeyboardInterrupt:
        console.print("Cancel...", style="bold red", justify="center")
        console.print("Goodbye!", style="bold red", justify="center")
        sys.exit(0)
        
if __name__ == '__main__':
    main()
