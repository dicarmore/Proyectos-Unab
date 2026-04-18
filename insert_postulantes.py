import sqlite3

# Ruta de la base de datos
DATABASE = 'database/respuestas.db'

# Datos ficticios para postulantes
postulantes = [
    {
        "rut": "12345678-9",
        "nombre": "Juan Pérez",
        "edad": 35,
        "profesion": "Ingeniero",
        "genero": "Masculino",
        "fecha_evaluacion": "2024-11-22",
        "terminal": "Santiago"
    },
    {
        "rut": "98765432-1",
        "nombre": "María López",
        "edad": 28,
        "profesion": "Conductora",
        "genero": "Femenino",
        "fecha_evaluacion": "2024-11-22",
        "terminal": "Valparaíso"
    },
    {
        "rut": "11111111-1",
        "nombre": "Carlos Gómez",
        "edad": 40,
        "profesion": "Mecánico",
        "genero": "Masculino",
        "fecha_evaluacion": "2024-11-23",
        "terminal": "Concepción"
    }
]

# Función para insertar postulantes en la base de datos
def insertar_postulantes():
    conn = sqlite3.connect(DATABASE)  # Conexión a la base de datos
    cursor = conn.cursor()

    # Insertar cada postulante en la tabla
    for postulante in postulantes:
        cursor.execute('''
            INSERT INTO postulantes (rut, nombre, edad, profesion, genero, fecha_evaluacion, terminal)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (postulante['rut'], postulante['nombre'], postulante['edad'], postulante['profesion'],
              postulante['genero'], postulante['fecha_evaluacion'], postulante['terminal']))

    conn.commit()  # Guardar cambios
    conn.close()  # Cerrar conexión
    print("Postulantes insertados con éxito.")

# Llamar a la función si se ejecuta el archivo directamente
if __name__ == '__main__':
    insertar_postulantes()
