import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Yspeed:

    def bestserveur(self):
        """
            FR:
                Récupère et retourne des informations détaillées sur l'adresse IP en utilisant le service https://www.speedtest.net/.
                Les informations récupérées incluent :
            
                   - Fournisseur : le nom du fournisseur d'accès à Internet de l'utilisateur, obtenu en utilisant Selenium.
                   - Serveur : le nom du serveur utilisé pour la connexion, également obtenu en utilisant Selenium.
                   
                Cette méthode utilise la bibliothèque 'requests' pour effectuer une requête HTTP et la bibliothèque 'selenium' pour interagir avec un navigateur web afin d'obtenir des informations supplémentaires, notamment le nom du fournisseur et le nom du serveur.
                
            EN:
            Retrieves and returns detailed IP address information using the https://www.speedtest.net/ service.
                Information retrieved includes:
                   - Provider: the name of the user's Internet Service Provider, obtained using Selenium.
                   - Server: the name of the server used for the connection, also obtained using Selenium.
                   
                This method uses the 'requests' library to make an HTTP request and the 'selenium' library to interact with a web browser to obtain additional information, including the provider name and server name.
        
        """
        driver = self._extracted_from_speedtest_10()
        go_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler') 
        go_button.click() 

        fournisseur = driver.find_element(By.CLASS_NAME, 'hostUrl').text 
        server = driver.find_element(By.CLASS_NAME, 'name').text 
 
        driver.quit() 

        return {
            "fournisseur": fournisseur,
            "Serveur": server,            
        } 
    
    def ipinfo(self):
        """
            FR:
                Récupère les informations sur l'adresse IP publique de l'utilisateur, telles que la ville, la région, le pays et l'opérateur.

                Cette fonction effectue une requête sur le service ipinfo.io pour obtenir des informations sur l'adresse IP publique de l'utilisateur.
                Les informations récupérées incluent l'adresse IP, la ville, la région, le pays et l'opérateur.

                Returns:
                    dict: Un dictionnaire contenant les informations sur l'adresse IP publique de l'utilisateur.
            EN:
                Retrieves information about the user's public IP address, such as city, region, country, and operator.

                This function makes a request to the ipinfo.io service to get information about the user's public IP address.
                The information retrieved includes IP address, city, region, country, and operator.

                Returns:
                    dict: A dictionary containing information about the user's public IP address.
        """
        
        response = requests.get("http://ipinfo.io/json")
        data = response.json() 
        ip_public = data['ip'] 
        city = data['city'] 
        region = data['region'] 
        country = data['country'] 
        operator = data['org']
        
        return {
            "ip": ip_public,
            "city": city,
            "region":  region,
            "country": country,
            "operator": operator,
        }
        
        
    def speedtest(self):
        """
            FR: 
                Récupère et retourne les résultats d'un test de vitesse de connexion Internet en utilisant le service en ligne Speedtest.
                Les informations récupérées incluent :
                    Vitesse de téléchargement : la vitesse à laquelle les données sont téléchargées depuis Internet vers l'ordinateur de l'utilisateur.
                    Vitesse d'envoi : la vitesse à laquelle les données sont envoyées depuis l'ordinateur de l'utilisateur vers Internet.
                    Ping : le temps de latence de la connexion, mesuré en millisecondes.
                    Cette méthode utilise la bibliothèque 'selenium' pour interagir avec un navigateur web et automatiser le test de vitesse sur le site Speedtest. Elle attend que le test soit terminé, extrait les résultats et ferme le navigateur avant de retourner les données.
                
            EN:
                Retrieves and returns the results of an Internet connection speed test using the online service Speedtest.
                The information retrieved includes:
                    Download Speed: The speed at which data is downloaded from the Internet to the user's computer.
                    Upload speed: the speed at which data is sent from the user's computer to the Internet.
                    Ping: the latency of the connection, measured in milliseconds.
                    This method uses the 'selenium' library to interact with a web browser and automate the speed test on the Speedtest site. It waits for the test to finish, extracts the results and closes the browser before returning the data.

        """
        
        driver = self._extracted_from_speedtest_10()
        rgpd_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        rgpd_button.click()
        go_button = driver.find_element(By.CSS_SELECTOR, '.start-button a')
        go_button.click()

        time.sleep(45)
        
        wait = WebDriverWait(driver, 10)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'result-data-large.number.result-data-value.download-speed')))
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'result-data-large.number.result-data-value.upload-speed')))
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'result-data-value.ping-speed')))


        
        download_speed = driver.find_element(By.CLASS_NAME, 'result-data-large.number.result-data-value.download-speed').text
        upload_speed = driver.find_element(By.CLASS_NAME, 'result-data-large.number.result-data-value.upload-speed').text
        ping_speed = driver.find_element(By.CLASS_NAME, 'result-data-value.ping-speed').text
        
        driver.quit()

        return {
            "download": download_speed,
            "upload": upload_speed,
            "ping": ping_speed,
        }

        

    # TODO Rename this here and in `ipinfo` and `speedtest`
    def _extracted_from_speedtest_10(self):
        """
            FR:
                Cette méthode privée (_extracted_from_speedtest_10) initialise un navigateur web en utilisant Selenium et charge le site Speedtest (https://www.speedtest.net/). Cette méthode est utilisée par les méthodes 'ipinfo' et 'speedtest' pour automatiser les interactions avec le site web.

                Les principales étapes de cette méthode sont les suivantes :

                   - Récupérer le nom du navigateur à partir des arguments de la ligne de commande, si disponible, sinon utiliser Chrome par défaut.
                   - Obtenir l'instance du webdriver correspondant au navigateur choisi en appelant la méthode get_webdriver.
                   - Charger le site Speedtest (https://www.speedtest.net/) à l'aide du webdriver.
                   - Attendre 5 secondes pour permettre au site de se charger correctement.
                   - La méthode retourne l'instance du webdriver initialisé et prêt à interagir avec le site Speedtest.
                   
            EN:
                This private method (_extracted_from_speedtest_10) initializes a web browser using Selenium and loads the Speedtest site (https://www.speedtest.net/). This method is used by the 'ipinfo' and 'speedtest' methods to automate interactions with the web site.

                The main steps of this method are as follows:

                   - Retrieve the browser name from the command line arguments, if available, otherwise use Chrome by default.
                   - Get the instance of the webdriver corresponding to the chosen browser by calling the get_webdriver method.
                   - Load the Speedtest site (https://www.speedtest.net/) using the webdriver.
                   - Wait 5 seconds to allow the site to load correctly.
                   - The method returns the instance of the webdriver initialized and ready to interact with the Speedtest site.
        """
        # Récupérer le nom du navigateur à partir des arguments de la ligne de commande, si disponible, sinon utiliser Chrome par défaut | Retrieve the browser name from the command line arguments, if available, otherwise use Chrome by default
        browser = sys.argv[1] if len(sys.argv) > 1 else "chrome"
        result = self.get_webdriver(browser)
        result.get("https://www.speedtest.net/")
        time.sleep(5)
        return result
                
               
            
    def get_webdriver(self,browser):
        """
            FR:
                Cette méthode (get_webdriver) est utilisée pour initialiser et retourner une instance de webdriver Selenium en fonction du navigateur spécifié en argument. Elle prend en charge les navigateurs Chrome, Firefox et Edge.

                Les principales étapes de cette méthode sont les suivantes :

                   - Vérifier quel navigateur a été spécifié en argument.
                   - Configurer les options du webdriver pour le navigateur choisi, notamment en activant le mode "headless" (sans interface utilisateur) et en désactivant certains niveaux de messages de la console.
                   - Retourner l'instance du webdriver configuré pour le navigateur choisi.
                   - Si le navigateur spécifié en argument n'est pas pris en charge, la méthode lèvera une exception ValueError.
                   
            EN:
                This method (get_webdriver) is used to initialize and return an instance of Selenium webdriver based on the browser specified in argument. It supports Chrome, Firefox and Edge browsers.

                    The main steps of this method are as follows:

                    - Check which browser has been specified as an argument.
                    - Configure the webdriver options for the chosen browser, including enabling headless mode and disabling some console message levels.
                    - Return the instance of the webdriver configured for the chosen browser.
                    - If the browser specified in the argument is not supported, the method will throw a ValueError exception.
                    
        """
        if browser.lower() == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            options.add_argument("--log-level=3") 
            options.add_experimental_option('excludeSwitches', ['enable-logging']) 
            return webdriver.Chrome(options=options)
        elif browser.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            options.log.level = "fatal"  
            return webdriver.Firefox(options=options)
        elif browser.lower() == "edge":
            options = webdriver.EdgeOptions()
            options.add_argument("--headless")
            options.add_argument("--log-level=3")  
            return webdriver.Edge(options=options)
        else:
            raise ValueError("Browser not supported")
        
        
    
if __name__ == '__main__':
    speedtest = Yspeed()
    print(speedtest.speedtest())
    print(speedtest.ipinfo())
    print(speedtest.best_server())