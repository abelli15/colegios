# Librerías
import os
from py_csv import read_csv, create_result_file, update_result_file, update_data_file
from py_chrome import open_browser, navigate_to_page, get_data, close_browser, get_maps_info

# 0) Variables globales
data_filename = os.path.join("files", "csv_codes_list.csv")
results_filename = os.path.join("files", "csv_codes_list_results.csv")
url_query = "https://gestiona.comunidad.madrid/wpad_pub/run/j/MostrarConsultaGeneral.icm"

# 1) Obtener el listado de códigos a consultar
data = read_csv(data_filename)

# 2) Crear el archivo donde se van a guardar los resultados
results = create_result_file(results_filename)

# 3) Buscar cada colegio
driver = open_browser()
index, total_len = 1, len(data)
for item in data:
    done, code = item["DONE"], item["ID"]
    print(str(index) + " de " + str(total_len) + "(" + code + ")")
    # Recoger el registro del archivo de salida (si ya existe)
    result = next((result for result in results if result["code"] == code), None)
    # Si no existe el registro, se hace la búsqueda del colegio
    if result is None:
        result = {
                    "code": code,
                    "name": "",
                    "tipo": "",
                    "titularidad": "",
                    "titular": "",
                    "territorio": "",
                    "dircc": "",
                    "tlf": "",
                    "fax": "",
                    "web": "",
                    "email": "",
                    "jornada": "",
                    "mncp": "",
                    "etps_educ": "",
                    "dist_coche": "",
                    "dist_trns_pub": "",
                    "dist_andnd": ""
                }
        navigate_to_page(driver, url_query)
        result["mncp"], result["etps_educ"], result["name"], result["tipo"], result["titularidad"], result["titular"], result["territorio"], result["dircc"], result["tlf"], result["fax"], result["web"], result["email"], result["jornada"] = get_data(driver, code)
        # Actualizar el csv de resultados
        results.append(result)
        update_result_file(results_filename, results)
    # Si no tiene información del maps, se hace la búsqueda de maps
    if result["dircc"] is not "" and (result["dist_coche"] is "" or result["dist_trns_pub"] is "" or result["dist_andnd"] is ""):
        result["dist_coche"], result["dist_trns_pub"], result["dist_andnd"] = get_maps_info(driver, result["dircc"])
        update_result_file(results_filename, results)
    index += 1
    if index % 50 == 0:
        close_browser(driver)
        driver = open_browser()

# 4) Cerrar el navegador
close_browser(driver)

