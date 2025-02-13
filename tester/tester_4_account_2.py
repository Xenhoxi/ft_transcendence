from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Exemple avec Chrome (tu peux remplacer par Firefox ou un autre navigateur)
# Assure-toi d'avoir téléchargé le WebDriver correspondant
driver_path = '/home/ljerinec/homebrew/bin/geckodriver'

firefox_binary_path = '/opt/firefox/stable/firefox/firefox'

# Créer une liste des comptes
comptes = [
    {'username': 'leon1', 'password': 'caca'},
    {'username': 'leon2', 'password': 'caca'},
    {'username': 'leon3', 'password': 'caca'},
    {'username': 'leon4', 'password': 'caca'}
]

# URL de la page de connexion de ton application
login_url = 'https://127.0.0.1:4443/'
game_url = 'https://127.0.0.1:4443/game'

# Liste pour stocker les instances des navigateurs
navigateurs = []

# Fonction pour se connecter à un compte
def se_connecter(navigateur, username, password):
    navigateur.get(login_url)
    # Trouver les champs de login et de mot de passe, puis se connecter
    champ_username = navigateur.find_element(By.NAME, 'username')  # Adapté selon ta page
    champ_password = navigateur.find_element(By.NAME, 'password')  # Adapté selon ta page

    champ_username.send_keys(username)
    champ_password.send_keys(password)
    
    bouton_login = navigateur.find_element(By.NAME, 'login')  # Adapté selon ta page
    bouton_login.click()

    time.sleep(0.5)
    navigateur.get(game_url)

    time.sleep(0.5)
    button_tournament = navigateur.find_element(By.ID, 'btn_tournament')
    button_tournament.click()

    time.sleep(0.5)
    button_tournament = navigateur.find_element(By.ID, 'start_research')
    button_tournament.click()


firefox_options = Options()
firefox_options.binary_location = firefox_binary_path

# Ouvrir les navigateurs et se connecter avec les comptes
for compte in comptes:
    service = Service(driver_path)
    navigateur = webdriver.Firefox(service=service, options=firefox_options) 
    navigateurs.append(navigateur)  # Stocke l'instance du navigateur
    se_connecter(navigateur, compte['username'], compte['password'])
    # time.sleep(2)  # Petit délai pour éviter de surcharger le serveur

# À ce stade, 4 fenêtres de navigateur devraient être ouvertes et chaque compte connecté

