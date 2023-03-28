"""Docstring for module Yspeed.
"""


import os
import platform
import sys
import time

import requests
from halo import Halo
from rich.console import Console
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from rich.text import Text
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Yspeed:
    """
    A class that provides methods to retrieve information about the user's,Internet connection speed and IP address.
    Methods:
        best_server():
            Retrieves and returns detailed IP address information using the https://www.speedtest.net/ service.
            Information retrieved includes:
            Provider: the name of the user's Internet Service Provider,obtained using Selenium.
            Server: the name of the server used for the connection,also obtained using Selenium.
            This method uses the 'requests' library to make an HTTP request and the 'selenium' library to interact with a web browser to obtain additional information, including the provider name and server name.
        get_ip_info():
            Retrieves information about the user's public IP address,such as city, region, country, and operator.
            This function makes a request to the ipinfo.io service to get information about the user's public IP address.
            The information retrieved includes IP address,city, region, country, and operator.
        Returns:
            dict: A dictionary containing information about the user's public IP address.
        get_speedtest():
            Retrieves and returns the results of an Internet connection speed test using the online service Speedtest.
            The information retrieved includes:
                Download Speed: The speed at which data is downloaded from the Internet to the user's computer.
                Upload speed: the speed at which data is sent from the user's computer to the Internet.
                Ping: the latency of the connection, measured in milliseconds.
                This method uses the 'selenium' library to interact with a web browser and automate the speed test on the Speedtest site.
                It waits for the test to finish, extracts the results and closes the browser before returning the data.
        _extracted_from_get_speedtest():
            A private method that initializes a web browser using Selenium and loads the Speedtest site (https://www.speedtest.net/).
            This method is used by the 'ipinfo' and 'speedtest' methods to automate interactions with the web site.
        get_webdriver(browser):
            This method is used to initialize and return an instance of Selenium webdriver based on the browser specified in argument.
             It supports Chrome, Firefox and Edge browsers.
    """

    def best_server(self) -> dict:
        """
        Retrieves and returns detailed IP address information using the https://www.speedtest.net/ service.
        Information retrieved includes:
        Provider: the name of the user's Internet Service Provider,obtained using Selenium.
        Server: the name of the server used for the connection,also obtained using Selenium.
        This method uses the 'requests' library to make an HTTP request and the 'selenium' library to interact with a web browser to obtain additional information,
        including the provider name and server name.
        """
        driver = self._extracted_from_get_speedtest()
        wait = WebDriverWait(driver, 5)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "hostUrl")))
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "name")))

        provider = driver.find_element(By.CLASS_NAME, "hostUrl").text
        server = driver.find_element(By.CLASS_NAME, "name").text

        driver.quit()

        return {"provider": provider, "Serveur": server}

    def get_ip_info(self) -> dict:
        """
        Retrieves information about the user's public IP address,such as city, region, country, and operator.
        This function makes a request to the ipinfo.io service to get information about the user's public IP address.
        The information retrieved includes IP address,city, region, country, and operator.
        Returns:
            dict: A dictionary containing information about the user's public IP address.
        """
        response = requests.get("https://ipinfo.io/json", timeout=5)
        data = response.json()
        ip_public = data["ip"]
        city = data["city"]
        region = data["region"]
        country = data["country"]
        operator = data["org"]
        return {
            "ip": ip_public,
            "city": city,
            "region": region,
            "country": country,
            "operator": operator,
        }

    def get_speedtest(self) -> dict:
        """
        Retrieves and returns the results of an Internet connection speed test using the online service Speedtest.
        The information retrieved includes:
            Download Speed: The speed at which data is downloaded from the Internet to the user's computer.
            Upload speed: the speed at which data is sent from the user's computer to the Internet.
            Ping: the latency of the connection, measured in milliseconds.
        This method uses the 'selenium' library to interact with a web browser and automate the speed test on the Speedtest site.
        It waits for the test to finish,extracts the results and closes the browser before returning the data.
        """
        driver = self._extracted_from_get_speedtest()
        go_button = driver.find_element(By.CSS_SELECTOR, ".start-button a")
        go_button.click()
        time.sleep(45)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.CLASS_NAME,
                    "result-data-large.number.result-data-value.download-speed",
                )
            )
        )
        wait.until(
            EC.visibility_of_element_located(
                (
                    By.CLASS_NAME,
                    "result-data-large.number.result-data-value.upload-speed",
                )
            )
        )
        wait.until(
            EC.visibility_of_element_located(
                (By.CLASS_NAME, "result-data-value.ping-speed")
            )
        )
        download_speed = driver.find_element(
            By.CLASS_NAME, "result-data-large.number.result-data-value.download-speed"
        ).text
        upload_speed = driver.find_element(
            By.CLASS_NAME, "result-data-large.number.result-data-value.upload-speed"
        ).text
        ping_speed = driver.find_element(
            By.CLASS_NAME, "result-data-value.ping-speed"
        ).text
        driver.quit()
        return {
            "download": download_speed,
            "upload": upload_speed,
            "ping": ping_speed,
        }

    def _extracted_from_get_speedtest(self) -> object:
        """
        A private method that initializes a web browser using Selenium and loads the Speedtest site (https://www.speedtest.net/).
        """
        result = self._extracted_from_speedtest()
        try:
            rgpd = result.find_element(By.ID, "onetrust-accept-btn-handler")

            rgpd.click()
            return result
        except NoSuchElementException:
            return result

    def run_speedtest(self):
        """Returns a dictionary containing the results of the speedtest."""
        total_iterations = 50
        # Frames pour le spinner personnalisé
        spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        # Utilisez Halo pour créer un spinner personnalisé
        try:
            with Halo(
                spinner={"interval": 100, "frames": spinner_frames},
                text="Starting the Speedtest",
                color="red",
                text_color="yellow",
            ).start() as spinner:
                time.sleep(1)
                for _ in range(total_iterations):
                    spinner.text = "Progression..."
                    speedtest = self.get_speedtest()
                    spinner.stop_and_persist(
                        text="Speedtest completed", symbol="✅".encode("utf-8")
                    )
                    return speedtest
        except (KeyboardInterrupt, SystemExit):
            spinner.stop_and_persist(
                text="Speedtest cancelled", symbol="❌".encode("utf-8")
            )
            return {
                "download": "N/A",
                "upload": "N/A",
                "ping": "N/A",
            }

    def display_results(self, speedtest: dict) -> None:
        """Displays the results of the speedtest in the console."""

        bold_yellow = "bold yellow"
        console = Console()
        console.print("\nSpeedtest", style=bold_yellow, justify="center")
        console.print(
            "Download: [bold green]{download}[/bold green]".format(**speedtest),
            style="blue",
            justify="center",
        )
        console.print(
            "Upload: [bold green]{upload}[/bold green]".format(**speedtest),
            style="blue",
            justify="center",
        )
        console.print(
            "Ping: [bold green]{ping}[/bold green]".format(**speedtest),
            style="blue",
            justify="center",
        )
        console.print("Thanks for Speedtest", style="bold red", justify="center")

    def define_brower(self) -> object:
        """
        Initialize and return an instance of Selenium webdriver based on the browser specified in argument.
        """
        system = platform.system().lower()
        if system == "windows":
            browser_executables = {
                "chrome": "chrome.exe",
                "firefox": "firefox.exe",
                "edge": "msedge.exe",
            }
            possible_paths = [
                os.path.join(
                    os.environ["ProgramFiles"], "Google", "Chrome", "Application"
                ),
                os.path.join(
                    os.environ["ProgramFiles(x86)"], "Google", "Chrome", "Application"
                ),
                os.path.join(os.environ["ProgramFiles"], "Mozilla Firefox"),
                os.path.join(os.environ["ProgramFiles(x86)"], "Mozilla Firefox"),
                os.path.join(
                    os.environ["ProgramFiles"], "Microsoft", "Edge", "Application"
                ),
                os.path.join(
                    os.environ["ProgramFiles(x86)"], "Microsoft", "Edge", "Application"
                ),
            ]
        elif system == "linux":
            browser_executables = {
                "chrome": "google-chrome",
                "firefox": "firefox",
                "edge": "microsoft-edge",
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

    def _extracted_from_speedtest(self) -> object:
        """
        This private method (_extracted_from_speedtest) initializes a web browser using Selenium and loads the Speedtest site(https://www.speedtest.net/).
        This method is used by the `ipinfo()` and `speedtest()` methods to automate interactions with the web site.
        The main steps of this method are as follows:
            Retrieve the browser name from the command line arguments,if available, otherwise use Chrome by default.
            Get the instance of the webdriver corresponding to the chosen browser by calling the get_webdriver method.
            Load the Speedtest site (https://www.speedtest.net/) using the webdriver.
            Wait 5 seconds to allow the site to load correctly.
            The method returns the instance of the webdriver initialized and ready to interact with the Speedtest site.
        """

        result = self.get_webdriver(self.define_brower())
        result.get("https://www.speedtest.net/")
        time.sleep(5)
        return result

    def get_webdriver(self, browser: str) -> object:
        """
        This method (get_webdriver) is used to initialize and return an instance of Selenium webdriver based on the browser specified in argument.
        It supports Chrome, Firefox and Edge browsers The main steps of this method are as follows:
            Check which browser has been specified as an argument.
        Configure the webdriver options for the chosen browser,including enabling headless mode and disabling some console message levels.
        Return the instance of the webdriver configured for the chosen browser.
        If the browser specified in the argument is not supported,the method will throw a ValueError exception.
        """
        if browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--log-level=3")
            # options.add_argument("--disable-dev-shm-usage")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
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
        raise ValueError("Browser not supported.")


class TimeElapsedColumnWithLabel(TimeElapsedColumn):
    """A column that displays the time elapsed since the task started."""

    def render(self, task) -> Text:
        elapsed = task.finished_time if task.finished else task.elapsed
        return Text("Time: {:.1f}s".format(elapsed))


def gather_network_info(speedtest: Yspeed, progress: Progress) -> dict:
    """Gathers the network information of the user."""
    with progress:
        task1 = progress.add_task(
            "Getting IP info...", title="[cyan]Getting IP info...", total=1
        )
        info = speedtest.get_ip_info()
        progress.update(task1, advance=1)
        task2 = progress.add_task(
            "Selecting best server...", title="[cyan]Selecting best server...", total=1
        )
        best = speedtest.best_server()
        progress.update(task2, advance=1)
        task3 = progress.add_task(
            "Performing speedtest...", title="[cyan]Performing speedtest...", total=1
        )
        speed = speedtest.get_speedtest()
        progress.update(task3, advance=1)
        return {
            **info,
            **best,
            **speed,
        }
    This function (print_network_info) prints the network information
    """
    clear_screen()
    bold_yellow = "bold yellow"
    console.print("Network Information", style=bold_yellow, justify="center")
    console.print(
        "Operator: [bold green]{operator}[/bold green]".format(**info),
        style="blue",
        justify="center",
    )
    console.print(
        "IP: [bold green]{ip}[/bold green]".format(**info),
        style="blue",
        justify="center",
    )
    console.print("\nLocalisation", style=bold_yellow, justify="center")
    console.print(
        "City: [bold green]{city}[/bold green]".format(**info),
        style="blue",
        justify="center",
    )
    console.print(
        "Region: [bold green]{region}[/bold green]".format(**info),
        style="blue",
        justify="center",
    )
    console.print(
        "Country: [bold green]{country}[/bold green]".format(**info),
        style="blue",
        justify="center",
    )
    console.print("\nBest Server", style=bold_yellow, justify="center")
    console.print(
        "Provider: [bold green]{provider}[/bold green]".format(**info),
        style="blue",
        justify="center",
    )
    console.print(
        "Server: [bold green]{Serveur}[/bold green]".format(**info),
        style="blue",
        justify="center",
    )
    console.print("\nSpeedTest", style=bold_yellow, justify="center")
    console.print(
        "Download: [bold green]{download} Mbps[/bold green]".format(**info),
        style="blue",
        justify="center",
    )
    console.print(
        "Upload: [bold green]{upload} Mbps[/bold green]".format(**info),
        style="blue",
        justify="center",
    )
    console.print(
        "Ping: [bold green]{ping} ms[/bold green]".format(**info),
        style="blue",
        justify="center",
    )


def _version() -> str:
    return "0.1.4"


def author() -> None:
    """
    Prints the name of the script author and their contact information.
    """
    console = Console()
    console.print("Author: Foufou-exe", style="grey35", justify="center")
    console.print(
        "Github: https://github.com/Foufou-exe", style="grey35", justify="center"
    )
    console.print(f"Version Yspeed: {_version()}", style="grey35", justify="center")


def clear_screen() -> None:
    """
    Clears the terminal screen based on the operating system.
    """
    system_name = platform.system()
    if system_name == "Windows":
        # do something specific for Windows

        os.system("cls")
    elif system_name == "Linux":
        # do something specific for Linux
        os.system("clear")
    else:
        print(f"Unable to clear the terminal because your system is not supported by the program. ({system_name})")

    
def main() -> None:
    """
    This function (main) is the main entry point of the script.
    """
    try:
        console = Console()
        speedtest = Yspeed()
        console.print("Welcome to Yspeed!", style="bold yellow", justify="center")
        author()

        console.print(
            "\n\nGathering network information...",
            style="bold yellow",
            justify="center",
        )
        with Progress(
            TextColumn("{task.fields[title]}"),
            BarColumn(),
            TimeElapsedColumnWithLabel(),
            console=console,
        ) as progress:
            info = gather_network_info(speedtest, progress)
        print_network_info(console, info)
    except (KeyboardInterrupt, SystemExit):
        clear_screen()
        console.print("Cancel...", style="bold red", justify="center")
        console.print("Goodbye!", style="bold red", justify="center")
        sys.exit(0)



if __name__ == "__main__":
    main()
