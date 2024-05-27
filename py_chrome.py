from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Variables globales
wait_XS = 1
wait_S = 5
wait_M = 10
wait_L = 30

# Funciones
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
