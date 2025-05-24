def carga(filename):
    try:
        with open(filename, "rb") as archivo:
            datos = archivo.read()
            return datos
    except IOError as e:
        print(f"Error al cargar el archivo: {e}")

def guarda(filename, contenido):
    try:
        with open(filename, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
    except IOError as e:
        print(f"Error al guardar el archivo: {e}")