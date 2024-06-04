import csv
from pathlib import Path

# Funciones generales
def read_csv(filename): # Leer el contenido de un archivo csv
    with open(filename, "r", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        data = list(reader)
    return data
def write_csv(filename, headers, data): # Escribir sobre un archivo csv (si no existe, se crea) a partir de un diccionario
    with open(filename, "w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)

# Funciones específicas
data_headers = ["ID", "DONE"]
results_headers = ["code", "name", "tipo", "titularidad", "titular", "territorio", "dircc", "tlf", "fax", "web", "email", "jornada", "mncp", "etps_educ", "dist_coche", "dist_trns_pub", "dist_andnd"]
def create_result_file(filename): # Crear el archivo de salida donde se van a guardar los resultados
    if Path(filename).is_file():
        results = read_csv(filename)
    else:
        results = []
        write_csv(filename, results_headers, results)   
    return results
def update_result_file(filename, results): # Actualiza el contenido del archivo de salida
    write_csv(filename, results_headers, results)
def update_data_file(filename, data): # Actualiza el contenido del archivo de entrada
    write_csv(filename, data_headers, data)
