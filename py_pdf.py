import os
import PyPDF2
import re
from py_csv import write_csv

def read_pdf(file_path): # Lee el contenido de un archivo PDF y devuelve el texto como una cadena
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
def extract_codes_from_text(text): # Extrae todos los códigos numéricos de 8 cifras del texto
    codes = re.compile(r"\b\d{8}\b").findall(text)
    return codes

pdf_text = read_pdf(os.path.join("files", "2023_06_maestros_ic_anexo_v_codigos_centros_y_localidades_e3325.pdf"))
codes = extract_codes_from_text(pdf_text)
codes_dict = []
for code in codes:
    codes_dict.append({"ID": code, "DONE": 0})
write_csv(os.path.join("files", "csv_codes_list.csv"), ["ID", "DONE"], codes_dict)

pass