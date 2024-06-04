from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Variables globales
wait_XS = 1
wait_S = 5
wait_M = 10
wait_L = 30

# Funciones generales
def open_browser(url=None):
    driver = webdriver.Chrome()
    if url is not None:
        driver.get(url)
    return driver
def navigate_to_page(driver, url):
    driver.get(url)
def find_element(driver, xpath, timeout=wait_L):
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
    return element
def find_elements(driver, xpath, timeout=wait_L):
    element = find_element(driver, xpath, timeout)
    elements = driver.find_elements(By.XPATH, xpath)
    return elements
def get_element_attribute(element, attribute):
    return element.get_attribute(attribute)
def click_element(driver, xpath, timeout=wait_L):
    element = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.XPATH, xpath)))
    element.click()
def send_keys_element(driver, xpath, keys, timeout=wait_L):
    element = find_element(driver, xpath, timeout)
    if keys.startswith("Keys_"):
        if keys.endswith("RETURN"):
            element.send_keys(Keys.RETURN)
    else:        
        element.send_keys(keys)
def get_html_text(driver, timeout=wait_L):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    return driver.page_source
def close_browser(driver):
    driver.quit()

# Funciones específicas
def get_data(driver, code): # Hacer la búsqueda por código de centro y obtener los datos de este
    click_element(driver, "//input[@id='basica.strCodNomMuni']")
    send_keys_element(driver, "//input[@id='basica.strCodNomMuni']", code)
    click_element(driver, "//a[@id='btnConsultarCritBusq01']")
    click_element(driver, f"//a[@onclick=\"enviarFormulario('{code}');\"]")
    name, tipo, titularidad, titular, mncp, dircc, tlf, fax, web, email, jornada = "", "", "", "", "", "", "", "", "", "", ""
    try: name, tipo, titularidad, titular, mncp, dircc, tlf, fax, web, email = get_capaDatIdentContent_values(find_element(driver, "//div[@id='capaDatIdentContent']").get_attribute("outerHTML"))
    except: pass
    try: jornada = get_capaOtrosCritContent_values(find_element(driver, "//div[@id='capaOtrosCritContent']").get_attribute("outerHTML"), wait_M)
    except: pass
    return name, tipo, titularidad, titular, mncp, dircc, tlf, fax, web, email, jornada
def get_capaDatIdentContent_values(capaDatIdentContent): # Obtener los datos name, tipo, titularidad, titular, mncp, dircc, tlf, fax, web, email
    name, tipo, titularidad, titular, mncp, dircc, tlf, fax, web, email = "", "", "", "", "", "", "", "", "", ""

    try:    
        soup = BeautifulSoup(capaDatIdentContent, "html.parser")

        name = soup.find(lambda tag: tag.name == "td" and "NOMBRE DEL CENTRO:" in tag.text).parent.find_next("tr").find("strong").text.strip().upper()
        tipo = soup.find(lambda tag: tag.name == "td" and "Tipo (denominación genérica):" in tag.text).find("strong").get_text(strip=True)
        titularidad = soup.find(lambda tag: tag.name == "td" and "Titularidad:" in tag.text).find_all("strong")[0].get_text(strip=True)
        titular = soup.find(lambda tag: tag.name == "td" and "Titular:" in tag.text).find_all("strong")[1].get_text(strip=True)
        mncp = soup.find(lambda tag: tag.name == "td" and "Área territorial:" in tag.text).find_all("strong")[1].get_text(strip=True)
        dircc = " ".join([strong.get_text(strip=True) for strong in soup.find(lambda tag: tag.name == "td" and "Dirección:" in tag.text).find_all("strong")])
        tlf = soup.find(lambda tag: tag.name == "td" and ("Teléfono:" in tag.text or "Teléfonos:" in tag.text)).find_all("strong")[0].get_text(strip=True)
        fax = soup.find(lambda tag: tag.name == "td" and "Fax:" in tag.text).find_all("strong")[1].get_text(strip=True)
        web = soup.find(lambda tag: tag.name == "td" and "Web:" in tag.text).find("a").get_text(strip=True)
        email = soup.find(lambda tag: tag.name == "td" and "Correo electrónico:" in tag.text).find_next_sibling("td").find("strong").get_text(strip=True)
    except:
        pass

    return name, tipo, titularidad, titular, mncp, dircc, tlf, fax, web, email
def get_capaOtrosCritContent_values(capaOtrosCritContent):  # Obtener los datos jornada
    jornada = ""
    
    try:
        soup = BeautifulSoup(capaOtrosCritContent, "html.parser")

        jornada_partida = " ".join(soup.find(lambda tag: tag.name == "span" and "Jornada dividida en 2 sesiones" in tag.text).get("class"))
        jornada_continua = " ".join(soup.find(lambda tag: tag.name == "span" and "Jornada continuada" in tag.text).get("class"))
        
        if jornada_partida == "pSizeS pNegro" and jornada_continua == "pSizeS pNegro":
            jornada = "Jornada partida y continua"
        elif jornada_partida == "pSizeS pGris" and jornada_continua == "pSizeS pGris":
            jornada = "Sin tipo de jornada identificada"
        elif jornada_partida == "pSizeS pNegro":
            jornada = "Jornada partida"
        elif jornada_continua == "pSizeS pNegro":
            jornada = "Jornada continua"
    except:
        pass

    return jornada

