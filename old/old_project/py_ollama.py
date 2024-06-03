from ollama import Client
from ollama import generate
import time

def configure_client(host="http://localhost:11434"):
    client = Client(host)
    return client
def generate_response(model="phi3",prompt="",system="",stream=False):
    start_time = time.time()  # Registro del tiempo de inicio
    response = generate(model=model,prompt=prompt,system=system,stream=stream)
    total_time = time.time() - start_time  # Cálculo del tiempo transcurrido
    print(total_time)
    return response

"""
web_text = ""

response = generate_response(model="phi3",
                    prompt="¿Encuentras información sobre el horario del colegio? Responde solo con 'sí' o 'no', nada más. El texto a analizar es este: " + web_text,
                    system="Estoy analizando el contenido de páginas webs de colegios para extraer información.",
                    stream=False)
print(response["response"])
if response["response"].upper().startswith("SI") or response["response"].upper().startswith("SÍ"):
    response = generate_response(model="phi3",
                    prompt="Me has dicho que en el siguiente texto hay información sobre el horario del colegio. Responde cuál es, solo el horario, nada más. El texto a analizar es este: " + web_text,
                    system="Estoy analizando el contenido de páginas webs de colegios para extraer información.",
                    stream=False)
pass
"""