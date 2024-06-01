import re
import time
from bs4 import BeautifulSoup
from py_ollama import generate_response

# Extraer la información relevante sobre horarios mediante Regex
def extract_schedules_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    soup = remove_script_tags(soup)

    # Patrones de horarios comunes
    pattern_1 = re.compile(r"horario", re.IGNORECASE)
    pattern_2 = re.compile(r"[0-9]{1,2}:[0-9]{2}")
    pattern_3 = re.compile(r"lunes|martes|miércoles|jueves|viernes|sábado|domingo")
    pattern_4 = re.compile(r"(ene(?:ro)?|feb(?:rero)?|mar(?:zo)?|abr(?:il)?|may(?:o)?|jun(?:io)?|jul(?:io)?|ago(?:sto)?|sep(?:tiembre)?|oct(?:ubre)?|nov(?:iembre)?|dic(?:iembre)?)", re.IGNORECASE)
    
    # Buscar nodos a partir de los patrones
    schedule_nodes = soup.find_all(text=re.compile(f'({pattern_1.pattern}|{pattern_2.pattern}|{pattern_3.pattern}|{pattern_4.pattern})', re.IGNORECASE))
    
    # Expandir la búsqueda a los padres de los nodos encontrados
    schedule_sections = []
    for node in schedule_nodes:
        parent = node.parent
        schedule_sections.append(str(parent))

    return " ".join(schedule_sections)
# Eliminar las etiquetas script
def remove_script_tags(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup

# Lee el contenido del archivo
test_file = "test_html.html"
with open(test_file, "r", encoding="utf-8") as file:
    html_content = file.read()

# Analiza el contenido HTML
schedule_info = extract_schedules_info(html_content)

# Pide a la IA que extraiga la información
schedule_prompt = "Si encuentras el horario lectivo del colegio, por favor, extrae únicamente el horario indicado. Si no encuentras nada, por favor, responde que no lo has encontrado. Debes buscar el horario lectivo en el siguiente HTML: " + schedule_info
start_time = time.time()
schedule_response = generate_response(model="phi3:3.8b",prompt=schedule_prompt,stream=False)
schedule_time = str(time.time() - start_time)
response = schedule_response["response"]
print(response)
pass