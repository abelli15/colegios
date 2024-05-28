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
web_text = "Coles Y Guardes\nColegios\nEscuelas Infantiles\nBlog\nNotas Cdi\nC.E.I.P. Joaquín Costa\nPÚBLICO\nDirección\nPaseo Pontones, 8, CP: 28005.\nDistrito Arganzuela, Madrid\nDatos de contacto\nTel.913653632\nFax.914053511\ncp.joaquincosta.madrid@educa.madrid.org\nWeb\nwww.colegiojoaquincosta.com/\nHorario\nHorario jornada lectiva\nDe Octubre a Mayo : 9:00-12:30 / 14:30-16:00 Septiembre y Junio: 9:00-13:00\nHorario ampliado\nAntes de la jornada lectiva: 7:30 – 9:00 ¿Se sirven desayunos?: Sí Precio del servicio: 45 € Después de la jornada lectiva: 16:00 - 17:00 Ejemplo de clases extraescolares ofertadas: Deportes, danza, dibujo, cuentacuentos, musicalia, teatro, francés, inglés… Precio aproximado de las clases extraescolares: De 13 € a 21 €. Natación: 49,5 €\nIdiomas\nColegio Bilingüe: Sí Programa BEDA: No Bilingüe en los cursos: En todos los cursos.\nHoras de inglés a la semana\nEn Infantil: Varias. En Primaria: 3 asignaturas (1/3 jormada).\nComedor\n¿Existe servicio de comedor? : Sí ¿ La comida se elabora en el centro? : Sí ¿Se elaboran menús especiales si existen problemas de salud?: Sí Precio aproximado del servicio de comedor: 5,50 €/día\nOtras Características\nNúmero de grupos por curso : 6 ¿Existe una zona específica de Infantil en el patio? : Sí ¿Después de comer se echan la siesta los pequeños?: Sí ¿Cómo se actúa si algún niño no controla perfectamente esfínteres?: Hay personal del AMPA que los cambia (50 € )\nOops! Something went wrong.\nThis page didn't load Google Maps correctly. See the JavaScript console for technical details.\nEsta web utiliza cookies para obtener datos estadísticos de la navegación de sus usuarios. Si continúas navegando consideramos que aceptas su uso. Más información X Cerrar\nAviso legal y política de privacidad\nPolítica de cookies"
#response = generate("phi3", "The next text is information about a school. I need the adress and the schedule in a single string each data. The text is this: " + web_text)
response = generate(model="phi3",
                    prompt="The text to find is this: " + web_text,
                    system="I need to obtain from a text the adress and the schedule. The format must be: 'Adress: ...' and 'Schedule: ...'. Be short and concise.",
                    stream=False)
print(response['response'])

response = client.chat(model="phi3", messages=[
  {
    "role": "user",
    "content": "Find adresses in the following text: 'Coles Y Guardes\nColegios\nEscuelas Infantiles\nBlog\nNotas Cdi\nC.E.I.P. Joaquín Costa\nPÚBLICO\nDirección\nPaseo Pontones, 8, CP: 28005.\nDistrito Arganzuela, Madrid\nDatos de contacto\nTel.913653632\nFax.914053511\ncp.joaquincosta.madrid@educa.madrid.org\nWeb\nwww.colegiojoaquincosta.com/\nHorario\nHorario jornada lectiva\nDe Octubre a Mayo : 9:00-12:30 / 14:30-16:00 Septiembre y Junio: 9:00-13:00\nHorario ampliado\nAntes de la jornada lectiva: 7:30 – 9:00 ¿Se sirven desayunos?: Sí Precio del servicio: 45 € Después de la jornada lectiva: 16:00 - 17:00 Ejemplo de clases extraescolares ofertadas: Deportes, danza, dibujo, cuentacuentos, musicalia, teatro, francés, inglés… Precio aproximado de las clases extraescolares: De 13 € a 21 €. Natación: 49,5 €\nIdiomas\nColegio Bilingüe: Sí Programa BEDA: No Bilingüe en los cursos: En todos los cursos.\nHoras de inglés a la semana\nEn Infantil: Varias. En Primaria: 3 asignaturas (1/3 jormada).\nComedor\n¿Existe servicio de comedor? : Sí ¿ La comida se elabora en el centro? : Sí ¿Se elaboran menús especiales si existen problemas de salud?: Sí Precio aproximado del servicio de comedor: 5,50 €/día\nOtras Características\nNúmero de grupos por curso : 6 ¿Existe una zona específica de Infantil en el patio? : Sí ¿Después de comer se echan la siesta los pequeños?: Sí ¿Cómo se actúa si algún niño no controla perfectamente esfínteres?: Hay personal del AMPA que los cambia (50 € )\nOops! Something went wrong.\nThis page didn't load Google Maps correctly. See the JavaScript console for technical details.\nEsta web utiliza cookies para obtener datos estadísticos de la navegación de sus usuarios. Si continúas navegando consideramos que aceptas su uso. Más información X Cerrar\nAviso legal y política de privacidad\nPolítica de cookies'",
  },
])
print(response["message"]["content"])
"""
