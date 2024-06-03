import re
from bs4 import BeautifulSoup

def find_match(pattern, string):
    match = re.search(pattern, string)
    return match
def find_all_matches(pattern, string):
    matches = re.findall(pattern, string)
    return matches
def replace_text(pattern, replacement, string):
    result = re.sub(pattern, replacement, string)
    return result
def split_text(pattern, string):
    result = re.split(pattern, string)
    return result
def match_pattern(pattern, string):
    match = re.fullmatch(pattern, string)
    return match
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
def remove_script_tags(soup):
    for script in soup(["script", "style"]):
        script.decompose()
    return soup
