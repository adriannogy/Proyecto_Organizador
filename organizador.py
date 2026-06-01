import os
import shutil

# 1. Definimos las carpetas de origen y destino
# Al poner solo el nombre, Python asume que están en la misma carpeta que este script
carpeta_origen = "Bandeja_Entrada"
carpeta_destino = "Documentos"
nombre_archivo = "prueba.txt"

# 2. Construimos las rutas exactas del archivo
ruta_origen = os.path.join(carpeta_origen, nombre_archivo)
ruta_destino = os.path.join(carpeta_destino, nombre_archivo)

# 3. Comprobamos si el archivo existe y lo movemos
if os.path.exists(ruta_origen):
    shutil.move(ruta_origen, ruta_destino)
    print(f"¡Magia! Se ha movido el archivo '{nombre_archivo}' a '{carpeta_destino}'.")
else:
    print(f"Ups, no encuentro el archivo en: {ruta_origen}. ¿Seguro que se llama así?")