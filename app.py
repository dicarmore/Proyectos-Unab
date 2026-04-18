import mysql.connector
from flask import Flask, render_template, request, redirect, url_for, session
import logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_sesion'

# Configuración de conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'D136o.84',  # Cambia esto por tu contraseña
    'database': 'cuestionario_db'
}

# Configuración de logs para depuración
logging.basicConfig(level=logging.DEBUG)

# Función para conectarse a la base de datos
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Ruta para mostrar la tabla `postulantes`
@app.route('/postulantes')
def ver_postulantes():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT * FROM postulantes ORDER BY nombre')
            postulantes = cursor.fetchall()
        return render_template('tabla.html', titulo='Postulantes', datos=postulantes)
    except mysql.connector.Error as e:
        logging.error(f"Error al obtener postulantes: {e}")
        return render_template('mensaje.html', mensaje="Error al obtener datos de postulantes.")

# Ruta para mostrar la tabla `preguntas`
@app.route('/preguntas')
def ver_preguntas():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('SELECT idP, texto AS Pregunta FROM preguntas ORDER BY idP')
            preguntas = cursor.fetchall()
        return render_template('tabla.html', titulo='Preguntas', datos=preguntas)
    except mysql.connector.Error as e:
        logging.error(f"Error al obtener preguntas: {e}")
        return render_template('mensaje.html', mensaje="Error al obtener datos de preguntas.")

# Ruta para mostrar la tabla `opciones`
@app.route('/opciones')
def ver_opciones():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute('''
                SELECT opciones.idO, opciones.texto, opciones.idP
                FROM opciones
                ORDER BY opciones.idP, opciones.idO
            ''')
            opciones = cursor.fetchall()
        return render_template('tabla.html', titulo='Opciones', datos=opciones)
    except mysql.connector.Error as e:
        logging.error(f"Error al obtener opciones: {e}")
        return render_template('mensaje.html', mensaje="Error al obtener datos de opciones.")

# Ruta para mostrar la tabla `respuestas`
@app.route('/respuestas')
def ver_respuestas():
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM respuestas ORDER BY fecha_evaluacion DESC')  # Ordenar por fecha y hora
        respuestas = cursor.fetchall()
    return render_template('tabla.html', titulo='Respuestas', datos=respuestas)

# Ruta para gestionar preguntas
@app.route('/gestionar_pregunta', methods=['GET', 'POST'])
def gestionar_pregunta():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                idP = request.form['idP']
                accion = request.form['accion']

                if accion == 'buscar':
                    cursor.execute('SELECT * FROM preguntas WHERE idP = %s', (idP,))
                    pregunta = cursor.fetchone()
                    return render_template('formulario_gestionar_pregunta.html', pregunta=pregunta, idP=idP)

                elif accion == 'guardar':
                    texto_pregunta = request.form['texto_pregunta'].strip()
                    cursor.execute('SELECT * FROM preguntas WHERE idP = %s', (idP,))
                    pregunta_existente = cursor.fetchone()

                    if pregunta_existente:
                        cursor.execute('UPDATE preguntas SET texto = %s WHERE idP = %s', (texto_pregunta, idP))
                        mensaje = f"Pregunta con ID {idP} actualizada correctamente."
                    else:
                        cursor.execute('INSERT INTO preguntas (idP, texto) VALUES (%s, %s)', (idP, texto_pregunta))
                        mensaje = f"Pregunta con ID {idP} agregada correctamente."

                    conn.commit()
                    return render_template('mensaje.html', mensaje=mensaje)
            return render_template('formulario_gestionar_pregunta.html', pregunta=None, idP=None)
    except mysql.connector.Error as e:
        logging.error(f"Error al gestionar preguntas: {e}")
        return render_template('mensaje.html', mensaje="Error al gestionar preguntas.")

# Ruta para gestionar opciones
@app.route('/gestionar_opcion', methods=['GET', 'POST'])
def gestionar_opcion():
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            if request.method == 'POST':
                idO = request.form['idO']
                accion = request.form['accion']

                if accion == 'buscar':
                    cursor.execute('SELECT * FROM opciones WHERE idO = %s', (idO,))
                    opcion = cursor.fetchone()
                    return render_template('formulario_gestionar_opcion.html', opcion=opcion, idO=idO)

                elif accion == 'guardar':
                    texto_opcion = request.form['texto_opcion'].strip()
                    idP = request.form['idP']
                    cursor.execute('SELECT * FROM opciones WHERE idO = %s', (idO,))
                    opcion_existente = cursor.fetchone()

                    if opcion_existente:
                        cursor.execute('UPDATE opciones SET texto = %s, idP = %s WHERE idO = %s', (texto_opcion, idP, idO))
                        mensaje = f"Opción con ID {idO} actualizada correctamente."
                    else:
                        cursor.execute('INSERT INTO opciones (idO, texto, idP) VALUES (%s, %s, %s)', (idO, texto_opcion, idP))
                        mensaje = f"Opción con ID {idO} agregada correctamente."

                    conn.commit()
                    return render_template('mensaje.html', mensaje=mensaje)
            return render_template('formulario_gestionar_opcion.html', opcion=None, idO=None)
    except mysql.connector.Error as e:
        logging.error(f"Error al gestionar opciones: {e}")
        return render_template('mensaje.html', mensaje="Error al gestionar opciones.")

# Ruta para el formulario principal
@app.route('/formulario/<int:pagina>', methods=['GET', 'POST'])
def formulario(pagina):
    # Inicializa las respuestas en la sesión si no existen
    if 'respuestas' not in session:
        session['respuestas'] = [None] * 57  # Inicializar respuestas vacías para 57 preguntas.

    if request.method == 'POST':
        if pagina == 1:
            # Capturar datos del postulante en la primera página
            session['rut'] = request.form.get('rut')
            session['apellido1'] = request.form.get('apellido1')
            session['apellido2'] = request.form.get('apellido2')
            session['nombres'] = request.form.get('nombres')
            session['fecha_evaluacion'] = request.form.get('fecha_evaluacion')
            session['edad'] = request.form.get('edad')
            session['profesion'] = request.form.get('profesion')
            session['genero'] = request.form.get('genero')
            session['terminal'] = request.form.get('terminal')

            # Depuración
            print(f"Datos del postulante recibidos: RUT={session['rut']}, "
                  f"Apellido1={session['apellido1']}, Apellido2={session['apellido2']}, "
                  f"Nombres={session['nombres']}, Fecha Evaluación={session['fecha_evaluacion']}, "
                  f"Edad={session['edad']}, Profesión={session['profesion']}, "
                  f"Género={session['genero']}, Terminal={session['terminal']}")

        # Capturar respuestas acumuladas desde el campo oculto
        respuestas_ocultas = request.form.get('respuestas_acumuladas', '').split('|')

        # Capturar respuestas de la página actual
        respuestas_pagina = request.form.to_dict(flat=True)
        for k, v in respuestas_pagina.items():
            if k.startswith('respuesta_'):
                index = int(k.split('_')[1]) - 1  # Extraer índice de la pregunta
                respuestas_ocultas[index] = v  # Actualizar respuesta en el índice correspondiente

        # Sincronizar respuestas acumuladas con la sesión
        session['respuestas'] = respuestas_ocultas

        # Depuración: Imprimir respuestas acumuladas
        print(f"Respuestas acumuladas hasta página {pagina}: {session['respuestas']}")

        # Redirigir a la siguiente página o guardar respuestas al finalizar
        if pagina == 6:  # Última página
            try:
                guardar_respuestas_finales(
                    session['rut'],
                    session['apellido1'],
                    session['apellido2'],
                    session['nombres'],
                    session['fecha_evaluacion'],
                    session['edad'],
                    session['profesion'],
                    session['genero'],
                    session['terminal'],
                    session['respuestas']
                )
                session.clear()  # Limpiar la sesión al finalizar
                return render_template('mensaje.html', mensaje="Formulario enviado con éxito.")
            except mysql.connector.Error as e:
                logging.error(f"Error al guardar respuestas: {e}")
                return render_template('mensaje.html', mensaje=f"Error al guardar respuestas: {e}")

        return redirect(url_for('formulario', pagina=pagina + 1))

    # Recuperar preguntas y opciones para la página actual
    inicio = (pagina - 1) * 10
    limite = 10 if pagina < 6 else 7

    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute('''
            SELECT preguntas.idP, preguntas.texto AS pregunta, opciones.idO, opciones.texto AS opcion
            FROM preguntas
            LEFT JOIN opciones ON preguntas.idP = opciones.idP
            WHERE preguntas.idP BETWEEN %s AND %s
            ORDER BY preguntas.idP, opciones.idO
        ''', (inicio + 1, inicio + limite))
        datos = cursor.fetchall()

    preguntas = {}
    for fila in datos:
        idP = fila['idP']
        if idP not in preguntas:
            preguntas[idP] = {'idP': idP, 'pregunta': fila['pregunta'], 'opciones': []}
        letra = ['A', 'B', 'C', 'D'][len(preguntas[idP]['opciones'])]  # Asignar letra según posición
        preguntas[idP]['opciones'].append({'idO': fila['idO'], 'letra': letra, 'texto': fila['opcion']})

    # Enviar respuestas acumuladas como campo oculto al formulario
    respuestas_ocultas = '|'.join([respuesta if respuesta else '' for respuesta in session['respuestas']])

    return render_template(
        'formulario_preguntas.html',
        preguntas=preguntas,
        pagina=pagina,
        respuestas_ocultas=respuestas_ocultas
    )


# Función para guardar respuestas en la base de datos
def guardar_respuestas_finales(rut, apellido1, apellido2, nombres, fecha_evaluacion, edad, profesion, genero, terminal, respuestas):
    # Usar fecha y hora actual
    fecha_hora_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Formato DATETIME

    # Reemplazar respuestas faltantes con ''
    respuestas_completadas = [respuesta if respuesta else '' for respuesta in respuestas]
    valores = [rut, apellido1, apellido2, nombres, fecha_hora_actual, edad, profesion, genero, terminal] + respuestas_completadas
    placeholders = ', '.join(['%s'] * len(valores))

    with get_db_connection() as conn:
        cursor = conn.cursor()
        query = f'''
            INSERT INTO respuestas (
                rut, apellido1, apellido2, nombres, fecha_evaluacion, edad, profesion, genero, terminal, 
                {", ".join([f"p{i}" for i in range(1, 58)])}
            ) VALUES ({placeholders})
        '''
        cursor.execute(query, valores)
        conn.commit()

# Página principal
@app.route('/')
def index():
    return """
    <h1>Bienvenido</h1>
    <ul>
        <li><a href='/postulantes'>Ver Postulantes</a></li>
        <li><a href='/preguntas'>Ver Preguntas</a></li>
        <li><a href='/opciones'>Ver Opciones</a></li>
        <li><a href='/respuestas'>Ver Respuestas</a></li>
        <li><a href='/gestionar_pregunta'>Gestionar Pregunta</a></li>
        <li><a href='/gestionar_opcion'>Gestionar Opción</a></li>
        <li><a href='/formulario/1'>Responder Formulario</a></li>
    </ul>
    """

if __name__ == '__main__':
    app.run(debug=True, port=5001)