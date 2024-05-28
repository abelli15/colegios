from py_chrome import open_browser,navigate_to_page,find_element,find_elements, get_element_attribute,click_element,send_keys_element,get_html_text,close_browser
from py_csv import read_csv,write_csv
from py_text import split_text,find_match

# Funciones
def google_search(driver, search_q):  ## Hacer búsqueda desde la página principal de google
    send_keys_element(driver, "//textarea[@name='q']", search_q)
    send_keys_element(driver, "//textarea[@name='q']", "Keys_RETURN")
def google_results(driver):
    urls = []
    results = find_elements(driver, "//a[@jsname='UWckNb']")
    for result in results:
        url = get_element_attribute(result, "href")
        urls.append(url)
    return urls

# Variables globales
input_filename = "csv_colegios_list copy.csv"  # Nombre del archivo CSV
output_filename = "csv_resultados.csv"         # Nombre del archivo de salida CSV
url_google = "https://www.google.com/"

# 1) Leer los datos del archivo CSV y crear el de salida
data = read_csv(input_filename)
output_headers = ["COLEGIO_NAME", "URL", "ADRESS", "SCHEDULE"]
results = []
write_csv(output_filename, output_headers, results)

# 2) Inicializar el navegador Chrome
driver = open_browser(url_google)
click_element(driver, "//button[@id='W0wltc']") # Quitar cookies

# 3) Buscar cada colegio y actualizar el CSV
for item in data:
    colegio_name = item["COLEGIO_NAME"]
    url = ""
    adresses = []
    schedules = []
    # 3.1) Buscar la web del colegio
    google_search(driver, colegio_name)    
    urls = google_results(driver)
    url = urls[0]
    navigate_to_page(driver, url)
    html_body = find_element(driver, "//body")
    html_text_list = split_text("\n", html_body.text)
    for html_text_element in html_text_list:
        # 3.2) Buscar la dirección del colegio
        adress_match = find_match(r"\b28[0-9]{3}\b", html_text_element)
        if adress_match:
            adresses.append(adress_match.string)
        # 3.3) Buscar el horario del colegio
        schedule_match = find_match(r"[0-9]{2}:[0-9]{2}", html_text_element)
        if schedule_match:
            schedules.append(schedule_match.string)
    # 3.4) Actualizar el CSV
    results.append({"COLEGIO_NAME": colegio_name, "URL": url, "ADRESS": adresses, "SCHEDULE": schedules})
    write_csv(output_filename, output_headers, results)
    # 3.5) Volver a la página principal de google
    navigate_to_page(driver, url_google)

# 4) Cerrar el navegador
close_browser(driver)