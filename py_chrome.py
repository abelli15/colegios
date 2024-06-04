from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

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

# Funciones web https://gestiona.comunidad.madrid/wpad_pub/run/j/MostrarConsultaGeneral.icm
def get_data(driver, code): # Hacer la búsqueda por código de centro y obtener los datos de este
    click_element(driver, "//input[@id='basica.strCodNomMuni']")
    send_keys_element(driver, "//input[@id='basica.strCodNomMuni']", code)
    click_element(driver, "//a[@id='btnConsultarCritBusq01']")
    mncp, etps_educ = "", ""
    try:
        general_info_element = find_element(driver, "//tr[@class='blanco pNegro pSizeM']")
        general_info_html = general_info_element.get_attribute("outerHTML")
        mncp, etps_educ = get_general_values(general_info_html)
    except Exception as e: print(f"get_data > get_general_values: {e}")
    click_element(driver, f"//a[@onclick=\"enviarFormulario('{code}');\"]")
    name, tipo, titularidad, titular, territorio, dircc, tlf, fax, web, email, jornada = "", "", "", "", "", "", "", "", "", "", ""
    try:
        capaDatIdentContent_element = find_element(driver, "//div[@id='capaDatIdentContent']")
        capaDatIdentContent_html = capaDatIdentContent_element.get_attribute("outerHTML")
        name, tipo, titularidad, titular, territorio, dircc, tlf, fax, web, email = get_capaDatIdentContent_values(capaDatIdentContent_html)
    except Exception as e: print(f"get_data > get_capaOtrosCritContent_values: {e}")
    try:
        capaOtrosCritContent_element = find_element(driver, "//div[@id='capaOtrosCritContent']", wait_M)
        capaOtrosCritContent_html = capaOtrosCritContent_element.get_attribute("outerHTML")
        jornada = get_capaOtrosCritContent_values(capaOtrosCritContent_html)
    except Exception as e: print(f"get_data > get_capaOtrosCritContent_values: {e}")
    return mncp, etps_educ, name, tipo, titularidad, titular, territorio, dircc, tlf, fax, web, email, jornada
def get_general_values(general_info): # Obtener los datos de mncp, etps_educ
    mncp, etps_educ = "", ""

    try:
        soup = BeautifulSoup(general_info, "html.parser")

        mncp = re.sub(r"[^\S ]+", "", soup.find_all("td", class_="pNegro pSizeM")[2].get_text(strip=True))
        etps_educ = " ".join([re.sub(r"[^\S ]+", "", span.get_text(strip=True)) for span in soup.find_all("td")[5].find_all("span")])
        if etps_educ == "":
            etps_educ = " ".join([re.sub(r"[^\S ]+", "", span.get_text(strip=True)) for span in soup.find_all("td")[6].find_all("span")])
            if etps_educ == "":
                pass

    except Exception as e:
            print(f"get_general_values: {e}")

    return mncp, etps_educ
def get_capaDatIdentContent_values(capaDatIdentContent): # Obtener los datos name, tipo, titularidad, titular, territorio, dircc, tlf, fax, web, email
    name, tipo, titularidad, titular, territorio, dircc, tlf, fax, web, email = "", "", "", "", "", "", "", "", "", ""

    try:    
        soup = BeautifulSoup(capaDatIdentContent, "html.parser")

        name = re.sub(r"[^\S ]+", "", soup.find(lambda tag: tag.name == "td" and "NOMBRE DEL CENTRO:" in tag.text).parent.find_next("tr").find("strong").text.strip().upper())
        tipo = re.sub(r"[^\S ]+", "", soup.find(lambda tag: tag.name == "td" and "Tipo (denominación genérica):" in tag.text).find("strong").get_text(strip=True))
        titularidad = re.sub(r"[^\S ]+", "", soup.find(lambda tag: tag.name == "td" and "Titularidad:" in tag.text).find_all("strong")[0].get_text(strip=True))
        titular = re.sub(r"[^\S ]+", "", soup.find(lambda tag: tag.name == "td" and "Titular:" in tag.text).find_all("strong")[1].get_text(strip=True))
        territorio = re.sub(r"[^\S ]+", "", soup.find(lambda tag: tag.name == "td" and "Área territorial:" in tag.text).find_all("strong")[1].get_text(strip=True))
        dircc = " ".join([re.sub(r"[^\S ]+", "", strong.get_text(strip=True)) for strong in soup.find(lambda tag: tag.name == "td" and "Dirección:" in tag.text).find_all("strong")])
        tlf = re.sub(r"[^\S ]+", "", soup.find(lambda tag: tag.name == "td" and ("Teléfono:" in tag.text or "Teléfonos:" in tag.text)).find_all("strong")[0].get_text(strip=True))
        fax = re.sub(r"[^\S ]+", "", soup.find(lambda tag: tag.name == "td" and "Fax:" in tag.text).find_all("strong")[1].get_text(strip=True))
        web = re.sub(r"[^\S ]+", "", soup.find(lambda tag: tag.name == "td" and "Web:" in tag.text).find("a").get_text(strip=True))
        email = re.sub(r"[^\S ]+", "", soup.find(lambda tag: tag.name == "td" and "Correo electrónico:" in tag.text).find_next_sibling("td").find("strong").get_text(strip=True))
    except Exception as e:
        print(f"get_capaDatIdentContent_values: {e}")

    return name, tipo, titularidad, titular, territorio, dircc, tlf, fax, web, email
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
    except Exception as e:
        print(f"get_capaOtrosCritContent_values: {e}")

    return jornada

# Funciones google maps
def get_maps_info(driver, dircc):
    dist_coche, dist_trns_pub, dist_andnd = "", "", ""

    url = "https://www.google.es/maps/dir/C.+del+Arroyo+de+la+Media+Legua,+46,+Moratalaz,+28030+Madrid/" + dircc.replace(" ", "+").replace("c/v","").replace("/","%2F")
    navigate_to_page(driver, url)

    try:
        if driver.current_url.startswith("https://consent.google.es/m"):
            click_element(driver, "//button[@aria-label='Rechazar todo']")
        dist_coche = re.sub(r"[^\S ]+", "", find_element(driver, "//div[@data-travel_mode='0']").text.strip())
        dist_trns_pub = re.sub(r"[^\S ]+", "", find_element(driver, "//div[@data-travel_mode='3']").text.strip())
        dist_andnd = re.sub(r"[^\S ]+", "", find_element(driver, "//div[@data-travel_mode='2']").text.strip())
    except Exception as e:
        print(f"get_maps_info: {e}")

    return dist_coche, dist_trns_pub, dist_andnd