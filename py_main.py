# Librerías
import os
from py_csv import read_csv, create_result_file, update_result_file, update_data_file
from py_chrome import open_browser, navigate_to_page, get_data, close_browser

# 0) Variables globales
data_filename = os.path.join("files", "csv_codes_list.csv")
results_filename = os.path.join("files", "csv_codes_list_results.csv")
url_query = "https://gestiona.comunidad.madrid/wpad_pub/run/j/MostrarConsultaGeneral.icm"

# 1) Obtener el listado de códigos a consultar
data = read_csv(data_filename)

# 2) Crear el archivo donde se van a guardar los resultados
results = create_result_file(results_filename)

# 3) Inicializar la web de búsqueda
driver = open_browser(url_query)

# 4) Buscar cada colegio
index, total_len = 0, len(data)
for item in data:
    done, code = item["DONE"], item["ID"]
    print(str(index) + " de " + str(total_len) + "(" + code + ")")
    if done == "0":
        # Buscar todos los datos sobre el colegio
        name, tipo, titularidad, titular, mncp, dircc, tlf, fax, web, email, jornada = "", "", "", "", "", "", "", "", "", "", ""
        try:
            navigate_to_page(driver, url_query)
            name, tipo, titularidad, titular, mncp, dircc, tlf, fax, web, email, jornada = get_data(driver, code)
        except:
            pass
        # Actualizar el csv de resultados
        results.append({"code": code, "name": name, "tipo": tipo, "titularidad": titularidad, "titular": titular, "mncp": mncp, "dircc": dircc, "tlf": tlf, "fax": fax, "web": web, "email": email, "jornada": jornada})
        update_result_file(results_filename, results)
        # Actualizar el csv de origen
        item["DONE"] = "1"
        update_data_file(data_filename, data)
    index += 1
    if index % 20 == 0:
        close_browser(driver)
        driver = open_browser(url_query)

# 5) Cerrar el navegador
close_browser(driver)

