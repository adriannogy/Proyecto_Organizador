import os
import shutil
import time
import PyPDF2  # <-- ¡NUEVA LIBRERÍA!
from google import genai
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# 1. Configuración de la IA
API_KEY = "Clave"
client = genai.Client(api_key=API_KEY)

CARPETA_ORIGEN = "Bandeja_Entrada"
CARPETAS_DESTINO = {
    "Facturas": os.path.join("Documentos", "Facturas"),
    "Apuntes": os.path.join("Documentos", "Apuntes"),
    "Personal": os.path.join("Documentos", "Personal")
}

for carpeta in CARPETAS_DESTINO.values():
    os.makedirs(carpeta, exist_ok=True)

# 3. El Vigilante Inteligente (Ahora lee PDFs)
class VigilanteArchivos(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
            
        ruta_archivo = event.src_path
        
        # AHORA ACEPTAMOS .TXT Y .PDF
        if not (ruta_archivo.lower().endswith('.txt') or ruta_archivo.lower().endswith('.pdf')):
            return
        
        time.sleep(2)
        if not os.path.exists(ruta_archivo) or os.path.getsize(ruta_archivo) == 0:
            return

        nombre_archivo = os.path.basename(ruta_archivo)
        print(f"\n[!] Nuevo archivo válido detectado: {nombre_archivo}")
        
        try:
            contenido = ""
            
            # --- NUEVA LÓGICA DE LECTURA ---
            if ruta_archivo.lower().endswith('.txt'):
                with open(ruta_archivo, "r", encoding="utf-8") as f:
                    contenido = f.read()
                    
            elif ruta_archivo.lower().endswith('.pdf'):
                # Los PDF se abren en modo "rb" (read binary)
                with open(ruta_archivo, "rb") as f:
                    lector_pdf = PyPDF2.PdfReader(f)
                    # Leemos solo las 2 primeras páginas para ser rápidos
                    paginas_a_leer = min(2, len(lector_pdf.pages))
                    for i in range(paginas_a_leer):
                        texto_pagina = lector_pdf.pages[i].extract_text()
                        if texto_pagina:
                            contenido += texto_pagina + "\n"
            # -------------------------------

            # Si el archivo no tiene texto (ej. es un PDF vacío o una foto escaneada)
            if not contenido.strip():
                print("[-] No pude extraer texto de este archivo. ¿Es una imagen escaneada?")
                return
                
            instrucciones = f"""
            Clasifica este texto en UNA categoría:
            - 'Facturas': Cobros, recibos, bancos.
            - 'Apuntes': Estudio, universidad, esquemas teóricos.
            - 'Personal': Listas de la compra, recordatorios, diarios.
            Responde SOLO con el nombre de la categoría exacta.
            Texto: {contenido}
            """
            
            print("Pensando y leyendo...")
            respuesta = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=instrucciones
            )
            categoria = respuesta.text.strip()
            
            if categoria in CARPETAS_DESTINO:
                ruta_destino = os.path.join(CARPETAS_DESTINO[categoria], nombre_archivo)
                if os.path.exists(ruta_archivo):
                    shutil.move(ruta_archivo, ruta_destino)
                    print(f"[+] Éxito. Archivo ordenado en: {categoria}")
            else:
                print(f"[-] Categoría desconocida: {categoria}")
                
        except Exception as e:
            print(f"Error procesando el archivo: {e}")

# 4. Arrancar
print(f"Vigilando la carpeta '{CARPETA_ORIGEN}'...")
print("¡Ahora acepto archivos .txt y .pdf! Arrastra uno para probar. (Ctrl+C para salir)")

observer = Observer()
observer.schedule(VigilanteArchivos(), CARPETA_ORIGEN, recursive=False)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
    print("\nBot apagado correctamente.")
observer.join()