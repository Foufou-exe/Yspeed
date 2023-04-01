# Code

#### Classe Yspeed

The constructor of the Yspeed class initializes the variables needed to perform a speed test, including the web browser, progress bar and browser options.

##### best_server(self) -> dict

```python linenums="1"
driver = self._extracted_from_get_speedtest()
wait = WebDriverWait(driver, 5)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "hostUrl")))
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "name")))

provider = driver.find_element(By.CLASS_NAME, "hostUrl").text
server = driver.find_element(By.CLASS_NAME, "name").text

driver.quit()

return {"provider": provider, "Serveur": server}
```

This method uses the __selenium__ library to interact with the web browser and get information about the best server for the connection. It returns a dictionary containing the server name.

##### display_results(self, speedtest: dict) -> None

```python linenums="1"
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
```

This method displays the results of the speed test in the console. It uses the __rich__ library to display the results in a readable format.

##### get_ip_info(self) -> dict

```python linenums="1"
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
```

This method uses the __requests__ library to make an HTTP request to an online service and retrieve information about the user's IP address, including city, region, country and operator. It returns a dictionary containing this information.

##### get_speedtest(self) -> dict

```python linenums="1"
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
```

This method uses the __selenium__ library to interact with the web browser and perform a speed test using the <https://www.speedtest.net/> service. It returns a dictionary containing the results of the speed test, including the download speed, upload speed and ping.

##### run_speedtest(self) -> dict

```python linenums="1"
total_iterations = 50
spinner_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
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
```

This method uses the __get_speedtest()__ method to perform a speed test and display a progress bar to indicate the progress of the test. It returns a dictionary containing the results of the speed test.

##### _extracted_from_get_speedtest(self) -> object

```python linenums="1"
result = self._extracted_from_speedtest()
try:
    rgpd = result.find_element(By.ID, "onetrust-accept-btn-handler")


    rgpd.click()
    return result
except NoSuchElementException:
    return result
```

This method is a private method that initializes a web browser using Selenium and loads the Speedtest site <https://www.speedtest.net/>.

##### _extracted_from_speedtest(self) -> object

```python linenums="1"
result = self.get_webdriver(self.define_brower())
result.get("https://www.speedtest.net/")
time.sleep(5)
return result
```

This method is a private method that uses the __selenium__ library to interact with the web browser and perform a speed test using the <https://www.speedtest.net/> service. It returns a __WebElement__ object containing the results of the speed test.

### Other function

##### main() -> None

```python linenums="1"
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
```

This function is the main function that is called when the script is run as a standalone program. It creates an instance of the __Yspeed__ class and calls the __run()__ method to perform the speed test.

##### gather_network_info(self, speedtest, progress_bar) -> dict

```python linenums="1"
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
```

This method uses the __get_ip_info()__, __best_server()__ and __get_speedtest()__ methods to retrieve information about the user's network and perform a speed test. It also uses a progress bar to display the progress of the test. It returns a dictionary containing all the information retrieved.

##### clear_screen() -> None

```python linenums="1"
system_name = platform.system()
if system_name == "Windows":
    # do something specific for Windows

    os.system("cls")
elif system_name == "Linux":
    # do something specific for Linux
    os.system("clear")
else:
    print(f"Unable to clear the terminal because your system is not supported by the program. ({system_name})")

```

This method clears the terminal screen depending on the operating system. It uses the __os__ library to call the appropriate system command to clear the screen.
