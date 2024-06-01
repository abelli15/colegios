from py_chrome import open_browser,navigate_to_page,find_element,find_elements, get_element_attribute,click_element,send_keys_element,get_html_text,close_browser
from py_csv import read_csv,write_csv
from py_text import extract_schedules_info
from py_ollama import generate_response
import time
import os.path
from pathlib import Path

# Funciones
def google_search(driver, search_q):  ## Hacer búsqueda desde la página principal de google
    send_keys_element(driver, "//textarea[@name='q']", search_q)
    send_keys_element(driver, "//textarea[@name='q']", "Keys_RETURN")
def google_results(driver): ## Obtener las URLs del resultado de la búsqueda
    urls = []
    results = find_elements(driver, "//a[@jsname='UWckNb']")
    for result in results:
        url = get_element_attribute(result, "href")
        urls.append(url)
    return urls
def create_output_file(output_filename): ## Crear el archivo de salida donde se van a guardar los resultados
    output_file = Path(output_filename)
    if output_file.is_file():
        results = read_csv(output_filename)
    else:
        results = []
    write_csv(output_filename, output_headers, results)
    return results
def find_schedule(html_content): ## Obtén el horario lectivo del HTML de la página
    schedule_info = extract_schedules_info(html_content)
    schedule_prompt = "Si encuentras el horario lectivo del colegio, por favor, extrae únicamente el horario indicado. Si no encuentras nada, por favor, responde que no lo has encontrado. Debes buscar el horario lectivo en el siguiente HTML: " + schedule_info
    start_time = time.time()
    schedule_response = generate_response(model="phi3:3.8b",prompt=schedule_prompt,stream=False)
    schedule_time = str(time.time() - start_time)
    response = schedule_response["response"]
    return(response, schedule_time)


# Variables globales
input_filename = "csv_colegios_list copy.csv" # Nombre del archivo CSV
input_headers = ["COLEGIO_NAME", "DONE"]
output_filename = "v3_csv_resultados.csv" # Nombre del archivo de salida CSV
output_headers = ["COLEGIO_NAME", "URL", "ADDRESS", "ADDRESS_TIME", "SCHEDULE", "SCHEDULE_TIME"]
url_google = "https://www.google.com/"
system_instruction = "Te voy a pasar el texto de la página web de un colegio y necesito que extraigas de él información. Tus respuestas deben ser breves, concisas y en una única línea. Si no encuentras nada, di que no has encontrado nada."

# 1) Leer los datos del archivo CSV y crear el de salida
data = read_csv(input_filename)
results = create_output_file(output_filename)

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
        colegio_name, url, address, address_time, schedule, schedule_time = item["COLEGIO_NAME"], "", "", "", "", ""
        try:
            # 4.1) Buscar la web del colegio
            google_search(driver, colegio_name)    
            urls = google_results(driver)
            url = urls[0]
            navigate_to_page(driver, url)
            html_content = get_html_text(driver)
            # 4.2) Buscar la dirección del colegio
            address = ""
            address_time = ""
            # 4.3) Buscar el horario del colegio
            schedule, schedule_time = find_schedule(html_content)
        except:
            pass
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
