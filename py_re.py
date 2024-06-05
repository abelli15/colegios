import re

def format_time(time_str):
    total_minutes, hours, mins = 0, 0, 0
    
    # Extraer las horas y los minutos teniendo en cuenta los diferentes formatos
    if "h" in time_str and "min" in time_str: # Ej: 1 h 5 min
        hours = int(re.search(r"(\d+)\s*h", time_str).group(1))
        mins = int(re.search(r"(\d+)\s*min", time_str).group(1))
    elif "h" in time_str and "y" in time_str: # Ej: 1 h y 5
        hours = int(re.search(r"(\d+)\s*h", time_str).group(1))
        mins = int(re.search(r"y\s*(\d+)", time_str).group(1))
    elif "min" in time_str: # Ej: 30 min
        mins = int(re.search(r"(\d+)\s*min", time_str).group(1))
    
    # Pasar el tiempo a minutos
    total_minutes = hours * 60 + mins

    return total_minutes