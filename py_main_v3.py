from py_chrome import open_browser,navigate_to_page,find_element,find_elements, get_element_attribute,click_element,send_keys_element,get_html_text,close_browser
from py_csv import read_csv,write_csv
from py_text import split_text,find_match
from py_ollama import configure_client,generate_response
import time
import os.path
from pathlib import Path

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
input_filename = "csv_colegios_list copy.csv" # Nombre del archivo CSV
input_headers = ["COLEGIO_NAME", "DONE"]
output_filename = "v3_csv_resultados.csv" # Nombre del archivo de salida CSV
output_headers = ["COLEGIO_NAME", "URL", "ADDRESS", "ADDRESS_TIME", "SCHEDULE", "SCHEDULE_TIME"]
url_google = "https://www.google.com/"
system_instruction = "Te voy a pasar el texto de la página web de un colegio y necesito que extraigas de él información. Tus respuestas deben ser breves, concisas y en una única línea. Si no encuentras nada, di que no has encontrado nada."

# 1) Leer los datos del archivo CSV y crear el de salida
data = read_csv(input_filename)
output_file = Path(output_filename)
if output_file.is_file():
    results = read_csv(output_filename)
else:
    results = []
write_csv(output_filename, output_headers, results)

# 2) Configurar ollama
#client = configure_client("http://localhost:11434")

# 3) Inicializar el navegador Chrome
driver = open_browser(url_google)
click_element(driver, "//button[@id='W0wltc']") # Quitar cookies

# 4) Buscar cada colegio y actualizar el CSV
total_len = len(data)
index = 0
for item in data:
    print(str(index) + " de " + str(total_len))
    index += 1
    done = item["DONE"]
    if done == "0":
        colegio_name = item["COLEGIO_NAME"]
        url = ""
        address = ""
        address_time = ""
        schedule = ""
        schedule_time = ""
        # 4.1) Buscar la web del colegio
        google_search(driver, colegio_name)    
        urls = google_results(driver)
        url = urls[0]
        navigate_to_page(driver, url)
        html_body = find_element(driver, "//body")
        # 4.2) Buscar la dirección del colegio
        address_prompt = "Extrae la direcciones física del colegio en el siguiente texto: " + html_body.text
        start_time = time.time()
        address_response = generate_response(model="phi3",prompt=address_prompt,system=system_instruction,stream=False)
        address_time = str(time.time() - start_time)
        address = address_response["response"]
        # 4.3) Buscar el horario del colegio
        schedule_prompt = "Extrae el horario del colegio en el siguiente texto: " + html_body.text
        start_time = time.time()
        schedule_response = generate_response(model="phi3",prompt=schedule_prompt,system=system_instruction,stream=False)
        schedule_time = str(time.time() - start_time)
        schedule = schedule_response["response"]
        # 4.4) Actualizar el CSV de resultados
        results.append({"COLEGIO_NAME": colegio_name, "URL": url, "ADDRESS": address, "ADDRESS_TIME": address_time, "SCHEDULE": schedule, "SCHEDULE_TIME": schedule_time})
        write_csv(output_filename, output_headers, results)
        # 4.5) Actualizar el CSV de origen
        item["DONE"] = "1"
        write_csv(input_filename, input_headers, data)
        # 4.5) Volver a la página principal de google
        navigate_to_page(driver, url_google)

# 4) Cerrar el navegador
close_browser(driver)
