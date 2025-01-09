from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Configurer le WebDriver
driver = webdriver.Chrome()

# Ouvrir la page de login
driver.get("http://localhost:4200/login")  # Remplacez avec l'URL de la page de connexion

# Attendre que la page se charge
time.sleep(5)

# Remplir les champs de connexion
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="nom d\'utilisateur"]').send_keys("admin2")
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="mot de passe"]').send_keys("admin2.password")

# Soumettre le formulaire de connexion
driver.find_element(By.CSS_SELECTOR, 'button[class="login-btn"]').click()

# Attendre que l'authentification soit réussie et que la page /add-dpi soit accessible
time.sleep(5)

driver.find_element(By.CSS_SELECTOR, 'button[id="addDPI"]').click()

# Attendre que la page se charge
time.sleep(5)

try:
    # Vérifier le titre de la page
    assert "Créer un nouveau DPI" in driver.page_source

    # Remplir les champs du formulaire
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="nom"]').send_keys("Dupont")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="prenom"]').send_keys("Jean")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="nss"]').send_keys("700")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="email"]').send_keys("jean.dupont@example.com")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="telephone"]').send_keys("0601020304")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="telephoneUrgence"]').send_keys("0708091011")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="adresse"]').send_keys("123 Rue de Paris")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="dateNaissance"]').send_keys("1980-05-10")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="medecinTraitant"]').send_keys("tenma")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="nomUtilisateur"]').send_keys("700")
    driver.find_element(By.CSS_SELECTOR, 'input[formControlName="motDePasse"]').send_keys("password123")
    driver.find_element(By.CSS_SELECTOR, 'textarea[formControlName="antécédents"]').send_keys("il est ienb")
    driver.find_element(By.CSS_SELECTOR, 'textarea[formControlName="mutuelle"]').send_keys("Mutuelle")

    # Soumettre le formulaire
    driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()

    # Attendre la réponse après soumission
    time.sleep(5)

    # Vérifier que le DPI a été créé avec succès (par exemple, un message de confirmation)
    assert "Le DPI est enregistré avec succès" in driver.page_source  # Modifiez selon le message réel affiché

    print("Test réussi : Le DPI a été créé avec succès.")

except AssertionError as e:
    print("Test échoué :", str(e))

finally:
    # Fermer le navigateur
    driver.quit()
