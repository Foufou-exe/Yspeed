# Code

#### Classe Yspeed

Le constructeur de la classe Yspeed initialise les variables nécessaires pour effectuer un test de vitesse, y compris le navigateur Web, la barre de progression et les options de navigateur.

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

Cette méthode utilise la bibliothèque __selenium__ pour interagir avec le navigateur Web et obtenir des informations sur le meilleur serveur pour la connexion. Elle retourne un dictionnaire contenant le nom du serveur.

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

Cette méthode affiche les résultats du test de vitesse dans la console. Elle utilise la bibliothèque __rich__ pour afficher les résultats dans un format lisible.

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

Cette méthode utilise la bibliothèque  __requests__ pour effectuer une requête HTTP à un service en ligne et récupérer des informations sur l'adresse IP de l'utilisateur, y compris la ville, la région, le pays et l'opérateur. Elle retourne un dictionnaire contenant ces informations.

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

Cette méthode utilise la bibliothèque __selenium__ pour interagir avec le navigateur Web et effectuer un test de vitesse en utilisant le service <https://www.speedtest.net/>. Elle retourne un dictionnaire contenant les résultats du test de vitesse, y compris la vitesse de téléchargement, la vitesse de téléversement et le ping.

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

Cette méthode utilise la méthode __get_speedtest()__ pour effectuer un test de vitesse et afficher une barre de progression pour indiquer l'état d'avancement du test. Elle retourne un dictionnaire contenant les résultats du test de vitesse.

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

Cette méthode est une méthode privée qui initialise un navigateur Web en utilisant Selenium et charge le site Speedtest <https://www.speedtest.net/>.

##### _extracted_from_speedtest(self) -> object

```python linenums="1"
result = self.get_webdriver(self.define_brower())
result.get("https://www.speedtest.net/")
time.sleep(5)
return result
```

Cette méthode est une méthode privée qui utilise la bibliothèque __selenium__ pour interagir avec le navigateur Web et effectuer un test de vitesse en utilisant le service <https://www.speedtest.net/>. Elle retourne un objet __WebElement__ contenant les résultats du test de vitesse.

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

Cette fonction est la fonction principale qui est appelée lorsque le script est exécuté en tant que programme autonome. Elle crée une instance de la classe __Yspeed__ et appelle la méthode __run()__ pour effectuer le test de vitesse.

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

Cette méthode utilise les méthodes __get_ip_info()__,__best_server()__ et __get_speedtest()__ pour récupérer des informations sur le réseau de l'utilisateur et effectuer un test de vitesse. Elle utilise également une barre de progression pour afficher l'état d'avancement du test. Elle retourne un dictionnaire contenant toutes les informations récupérées.

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

Cette méthode efface l'écran du terminal en fonction du système d'exploitation. Elle utilise la bibliothèque __os__ pour appeler la commande système appropriée pour effacer l'écran.
