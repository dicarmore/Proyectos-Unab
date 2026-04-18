from flask import Flask, request, render_template
import mysql.connector
import logging

app = Flask(__name__)

# Configuración de conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="D136o.84",
        database="cuestionario_db"
    )

# Ruta para el formulario de búsqueda y consulta
@app.route('/consulta', methods=['GET', 'POST'])
def consulta_resultados():
    resultado = None  # Variable para almacenar el resultado de la búsqueda
    mensaje_error = None  # Variable para manejar mensajes de error
    respuestas_por_fila = []  # Lista para almacenar las respuestas en formato fila
    suma_positivos = 0  # Inicializar suma de puntajes positivos
    suma_negativos = 0  # Inicializar suma de puntajes negativos

    # Definir puntajes para las preguntas (esto debe completarse con los puntajes para todas las preguntas)
    PUNTAJES = [
        {"A": 1, "B": 2, "C": 3, "D": -3},  # Ejemplo para pregunta 1
        {"A": 2, "B": 1, "C": -1, "D": -3},  # Ejemplo para pregunta 2
        # Agrega los puntajes restantes aquí...
    ]

    if request.method == 'POST':
        rut = request.form.get('rut')
        if not rut:
            mensaje_error = "Por favor, ingrese un RUT válido."
        else:
            try:
                with get_db_connection() as conn:
                    cursor = conn.cursor(dictionary=True)
                    # Obtener información del postulante
                    cursor.execute('''
                        SELECT rut, apellido1, apellido2, nombres, fecha_evaluacion, 
                               edad, profesion, genero, terminal,
                               p1, p2, p3, p4, p5, p6, p7, p8, p9, p10,
                               p11, p12, p13, p14, p15, p16, p17, p18, p19, p20,
                               p21, p22, p23, p24, p25, p26, p27, p28, p29, p30,
                               p31, p32, p33, p34, p35, p36, p37, p38, p39, p40,
                               p41, p42, p43, p44, p45, p46, p47, p48, p49, p50,
                               p51, p52, p53, p54, p55, p56, p57
                        FROM respuestas
                        WHERE rut = %s
                        ORDER BY fecha_evaluacion DESC
                        LIMIT 1
                    ''', (rut,))
                    resultado = cursor.fetchone()

                    if resultado:
                        # Transformar las respuestas en formato de filas
                        for i in range(1, 58):  # De p1 a p57
                            respuesta = resultado[f"p{i}"]
                            respuestas_por_fila.append({
                                "#": i,
                                "A": "X" if respuesta == "A" else "",
                                "B": "X" if respuesta == "B" else "",
                                "C": "X" if respuesta == "C" else "",
                                "D": "X" if respuesta == "D" else ""
                            })

                            # Calcular puntajes si está definido en PUNTAJES
                            if i <= len(PUNTAJES):  # Evitar índices fuera de rango
                                puntaje = PUNTAJES[i - 1].get(respuesta, 0)
                                if puntaje > 0:
                                    suma_positivos += puntaje
                                elif puntaje < 0:
                                    suma_negativos += puntaje
                    else:
                        mensaje_error = f"No se encontraron resultados para el RUT: {rut}"
            except mysql.connector.Error as e:
                logging.error(f"Error al consultar resultados: {e}")
                mensaje_error = "Ocurrió un error al realizar la consulta."

    return render_template(
        'consulta_resultados.html',
        resultado=resultado,
        respuestas_por_fila=respuestas_por_fila,
        suma_positivos=suma_positivos,
        suma_negativos=suma_negativos,
        mensaje_error=mensaje_error
    )

if __name__ == '__main__':
    app.run(port=5001, debug=True)