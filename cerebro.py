import os
from google import genai

# 1. Configurar la IA (Nueva sintaxis)
# PEGA AQUÍ TU *NUEVA* CLAVE SECRETA (¡Y no la compartas en ningún foro o chat!)
API_KEY = "Clave"
client = genai.Client(api_key=API_KEY)

# 2. Leer el archivo de tu bandeja de entrada
ruta_archivo = os.path.join("Bandeja_Entrada", "prueba.txt")

with open(ruta_archivo, "r", encoding="utf-8") as archivo:
    contenido_texto = archivo.read()

print(f"He leído el archivo. El texto es: '{contenido_texto}'")
print("Pensando...")

# 3. Darle instrucciones a la IA (El Prompt)
instrucciones = f"""
Eres un asistente que clasifica documentos. 
Lee el siguiente texto y clasifícalo en UNA de estas tres categorías:
- 'Facturas': Todo lo relacionado con cobros, recibos, bancos o compras formales.
- 'Apuntes': Textos de estudio, universidad, colegio, esquemas o resúmenes teóricos.
- 'Personal': Cosas del día a día, listas de la compra, recordatorios de casa o diarios.

Responde SOLO con la categoría exacta, sin puntos ni comillas.
Texto: {contenido_texto}
"""

# 4. Obtener y mostrar la respuesta (¡Cambiamos a la versión actual 2.5-flash!)
respuesta = client.models.generate_content(
    model='gemini-2.5-flash',
    contents=instrucciones
)

categoria = respuesta.text.strip()
print(f"¡Clasificación completada! La IA dice que esto es: {categoria}")