import sqlite3

# Ruta de la base de datos
DATABASE = 'database/respuestas.db'

# Respuestas ficticias
respuestas = [
    {
        "rut": "12345678-9",
        "fecha_evaluacion": "2024-11-22",
        "respuestas": ["A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D",
                       "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D",
                       "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C", "D", "A", "B", "C"]
    },
    {
        "rut": "98765432-1",
        "fecha_evaluacion": "2024-11-22",
        "respuestas": ["D", "C", "B", "A", "D", "C", "B", "A", "D", "C", "B", "A", "D", "C", "B", "A", "D", "C", "B", "A",
                       "D", "C", "B", "A", "D", "C", "B", "A", "D", "C", "B", "A", "D", "C", "B", "A", "D", "C", "B", "A",
                       "D", "C", "B", "A", "D", "C", "B", "A", "D", "C", "B", "A", "D", "C", "B"]
    }
]

# Función para completar las respuestas faltantes con "N/A"
def completar_respuestas(respuestas, total=57):
    return respuestas + ["N/A"] * (total - len(respuestas))

# Función para insertar respuestas en la base de datos
def insertar_respuestas():
    conn = sqlite3.connect(DATABASE)  # Conexión a la base de datos
    cursor = conn.cursor()

    # Insertar cada conjunto de respuestas en la tabla
    for respuesta in respuestas:
        # Completar respuestas faltantes
        respuestas_completas = completar_respuestas(respuesta['respuestas'])

        # Crear una tupla con rut, fecha_evaluacion y todas las respuestas
        valores = (respuesta['rut'], respuesta['fecha_evaluacion'], *respuestas_completas)

        # Verificar que la cantidad de valores sea 59
        assert len(valores) == 59, f"Número incorrecto de valores: {len(valores)} (se esperaban 59)."

        cursor.execute(f'''
            INSERT INTO respuestas (rut, fecha_evaluacion, {', '.join([f'p{i}' for i in range(1, 58)])})
            VALUES ({', '.join(['?' for _ in range(59)])})
        ''', valores)

    conn.commit()  # Guardar cambios
    conn.close()  # Cerrar conexión
    print("Respuestas insertadas con éxito.")

# Llamar a la función si se ejecuta el archivo directamente
if __name__ == '__main__':
    insertar_respuestas()
