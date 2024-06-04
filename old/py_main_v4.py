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

# 3) Inicializar la web de búsqueda
driver = open_browser(url_query)

# 4) Buscar cada colegio
index, total_len = 1, len(data)
for item in data:
    done, code = item["DONE"], item["ID"]
    print(str(index) + " de " + str(total_len) + "(" + code + ")")
    # Buscar todos los datos sobre el colegio
    mncp, etps_educ, name, tipo, titularidad, titular, territorio, dircc, tlf, fax, web, email, jornada, dist_coche, dist_trns_pub, dist_andnd = "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
    if done == "0":
        try:
            navigate_to_page(driver, url_query)
            mncp, etps_educ, name, tipo, titularidad, titular, territorio, dircc, tlf, fax, web, email, jornada = get_data(driver, code)
            item["DONE"] = "1"
        except Exception as e:
            print(f"get_data: {e}")
        # Actualizar el csv de resultados
        results.append({"code": code, "name": name, "tipo": tipo, "titularidad": titularidad, "titular": titular, "territorio": territorio, "dircc": dircc, "tlf": tlf, "fax": fax, "web": web, "email": email, "jornada": jornada, "mncp": mncp, "etps_educ": etps_educ, "dist_coche": dist_coche, "dist_trns_pub": dist_trns_pub, "dist_andnd": dist_andnd})
        update_result_file(results_filename, results)
        # Actualizar el csv de origen
        update_data_file(data_filename, data)
    else:
        dircc = (result["dircc"] for result in results if result["code"] == code)
    # Buscar las distancias a las que está el colegio
    if dircc is not "":
        dist_coche, dist_trns_pub, dist_andnd = get_maps_info(driver, dircc)
    
    index += 1
    if index % 40 == 0:
        close_browser(driver)
        driver = open_browser(url_query)

# 5) Cerrar el navegador
close_browser(driver)

