import mysql.connector

# Configuración de conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Cambia esto si usaste otro usuario
    'password': 'D136o.84',  # Cambia esto por la contraseña que configuraste
    'database': 'cuestionario_db'
}

def inicializar_base_datos():
    print("Conectando a la base de datos...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    try:
        print("Eliminando tablas antiguas (si existen)...")
        cursor.execute('DROP TABLE IF EXISTS respuestas')
        cursor.execute('DROP TABLE IF EXISTS opciones')
        cursor.execute('DROP TABLE IF EXISTS preguntas')
        cursor.execute('DROP TABLE IF EXISTS postulantes')

        print("Creando tabla 'postulantes'...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS postulantes (
                rut VARCHAR(20) PRIMARY KEY,
                nombre VARCHAR(100) NOT NULL,
                edad INT NOT NULL,
                profesion VARCHAR(100) NOT NULL,
                genero ENUM('Masculino', 'Femenino', 'Otro') NOT NULL,
                fecha_evaluacion DATE NOT NULL,
                terminal VARCHAR(50) NOT NULL
            )
        ''')

        print("Creando tabla 'preguntas'...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS preguntas (
                idP INT AUTO_INCREMENT PRIMARY KEY,
                texto VARCHAR(255) NOT NULL
            )
        ''')

        print("Creando tabla 'opciones'...")
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS opciones (
                idO VARCHAR(10) PRIMARY KEY,
                texto VARCHAR(255) NOT NULL,
                idP INT NOT NULL,
                FOREIGN KEY (idP) REFERENCES preguntas(idP)
            )
        ''')

        print("Creando tabla 'respuestas'...")
        # Tabla de respuestas con columnas p1, p2, ..., p57
        columnas_respuestas = ', '.join([f'p{i} VARCHAR(1)' for i in range(1, 58)])  # p1 a p57
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS respuestas (
                rut VARCHAR(20) NOT NULL,
                fecha_evaluacion DATE NOT NULL,
                {columnas_respuestas},
                PRIMARY KEY (rut, fecha_evaluacion),
                FOREIGN KEY (rut) REFERENCES postulantes(rut)
            )
        ''')

        # Verificar las tablas creadas
        cursor.execute("SHOW TABLES")
        tablas = cursor.fetchall()
        print("Tablas creadas en la base de datos:", [tabla[0] for tabla in tablas])

        conn.commit()
        print("Base de datos actualizada correctamente.")

    except mysql.connector.Error as e:
        print(f"Error durante la inicialización de la base de datos: {e}")

    finally:
        cursor.close()
        conn.close()
        print("Conexión a la base de datos cerrada.")

# Ejecutar la función si el archivo es ejecutado directamente
if __name__ == '__main__':
    inicializar_base_datos()