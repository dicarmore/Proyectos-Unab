import mysql.connector

# Configuración de conexión a MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Cambia esto si usaste otro usuario
    'password': 'D136o.84',  # Cambia esto por la contraseña que configuraste
    'database': 'cuestionario_db'
}

# Lista completa de preguntas (del 1 al 57)
preguntas = [
    "Soy prudente, ante todo, cuando...",
    "Me muestro imperturbable y tranquilo...",
    "Me impaciento cuando...",
    "Mi comportamiento es...",
    "Me muestro intolerante ante conductores...",
    "Cuando tengo prisa...",
    "Conduciendo soy sobre todo cortés con...",
    "Mi conducta es intransigente con...",
    "Insulto -aunque no lo oigan- a otros conductores cuando...",
    "Me pongo nervioso e impaciente conduciendo...",
    "Si llevo prisa, lo que más me molesta es que...",
    "Llamo la atención a los conductores que...",
    "Recrimino sin piedad la actuación de los conductores...",
    "Me siento más contento conmigo mismo cuando...",
    "Me molesta que...",
    "Me comporto agresivamente si...",
    "Tiendo a arriesgarme habitualmente...",
    "Extremo las medidas de seguridad...",
    "Cuando llevo prisa...",
    "Me muestro inseguro con el coche...",
    "Usted está maniobrando para estacionar su coche en la calle, pero otros usuarios le pitan reiteradamente...",
    "Se encuentra ante una confluencia vial, con la señal 'ceda el paso' y tráfico intenso...",
    "Intenta aparcar en el lugar que acaba de ocupar libre, pero otro automovilista más 'listillo' se le adelanta...",
    "Está ante un semáforo verde, pero el agente de tráfico retiene la circulación unos minutos, sin motivo aparente...",
    "Va conduciendo normalmente en carretera; inesperadamente se le coloca delante otro usuario haciéndole realizar una brusca acción evasiva...",
    "Conduciendo en caravana detrás de un vehículo lento, al intentar adelantarle, otros vehículos se le adelantan, le impiden el paso e incluso le pitan...",
    "Conduciendo por el carril central de una carretera de doble vía a una velocidad reglamentaria, otro automovilista le da reiteradamente señales de luces para que se retire a un lado...",
    "Conduciendo con normalidad por carretera, ve cómo el agente de tráfico le adelanta, y le indica que se detenga...",
    "Sale de viaje y algún miembro de su familia le va haciendo constantemente observaciones y recriminaciones...",
    "Se encuentra en uno de los muchos atascos urbanos y ve cómo pasa el tiempo y apenas avanza...",
    "Por la mañana, debido a la densidad de tráfico urbano, no puede llegar puntual a su destino...",
    "Va conduciendo bastante lentamente por la carretera; otros automovilistas de atrás le pitan o dan las luces...",
    "Se encuentra ante una interrupción de tráfico sin conocer las causas; no obstante, ve cómo algunos automovilistas se cuelan por el arcén y continúan...",
    "Conduciendo, le sigue detrás otro vehículo que intenta adelantarle; le indica Ud. la presencia de vehículos en sentido contrario y, sin embargo, insiste...",
    "De repente tiene que frenar ante la presencia de un peatón que se cruza y éste ni se inmuta...",
    "El conductor que va delante, da un frenazo bruscamente y Ud. se empotra en la parte trasera, sin que pueda evitarlo...",
    "Se acaba de poner para Ud. el semáforo en rojo; no obstante, observa que algunos peatones cruzan sin prisas, haciéndole esperar...",
    "Otro automovilista le adelanta, haciéndolo de forma temeraria, y se coloca delante de su vehículo; Ud. trata de frenar y le alcanza causándole desperfectos...",
    "Conduciendo con normalidad, de pronto otro automovilista, que no ha calculado bien, le alcanza lateralmente, causándole grandes daños en su coche...",
    "Conduciendo en zona urbana con señal de velocidad limitada, va ligeramente por encima de lo indicado. El agente de tráfico le detiene...",
    "Se encuentra un semáforo en intermitencia y en verde para peatones...",
    "Va a adelantar a otro vehículo, pero cuando lo intenta, éste se lo impide a propósito aumentando la velocidad...",
    "Otro conductor hace que Ud. cometa una acción evasiva (o cometa una infracción) y no le pide disculpas...",
    "En una autovía, con carril para vehículos lentos, se encuentra con un camión que no hace uso de dicho carril, obstruyendo el paso...",
    "Va conduciendo acompañado de gente que le va distrayendo constantemente...",
    "Se encuentra detrás de un conductor 'novato' ante un semáforo que se pone en verde, pero tarda bastante en iniciar la marcha...",
    "En caravana, Ud. y otros conductores han cedido el paso a una ambulancia; sin embargo, otros que vienen detrás aprovechan la ocasión y le obstaculizan para incorporarse al carril...",
    "Al intentar salir, encuentra un coche aparcado en doble fila que le impide su salida durante un buen rato...",
    "Conduciendo de noche, otro vehículo que viene en sentido contrario le deslumbra, Ud. le avisa de ello, pero él no se da por enterado...",
    "Al intentar adelantar a un autobús, éste de inmediato da la intermitencia, para y gira a la izquierda...",
    "De noche, una vez que ha adelantado a otro vehículo, éste mantiene las luces largas, deslumbrándole un buen rato...",
    "Va a entrar por una calle de dirección única, pero otro coche viene por ella, haciendo caso omiso de la señal de prohibido...",
    "Conduciendo en caravana, ve cómo otros vehículos vienen adelantando por el arcén hasta que les obstaculiza otro aparcado en él, entonces intentan colocarse delante de Ud....",
    "En día de niebla abundante va conduciendo en carretera detrás de un vehículo largo...",
    "En un día de lluvia, al pasar por un charco, empapa a los peatones que pasan por la acera...",
    "Deja su coche estacionado en casco urbano; al regresar se encuentra con un agente multándole...",
    "Se acerca a un cruce en el cual tiene preferencia; sin embargo, viene otro usuario que no parece dispuesto a cederle el paso..."
]

# Función para insertar preguntas en la base de datos
def insertar_preguntas():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    for idP, texto in enumerate(preguntas, start=1):  # Empieza desde la pregunta 1
        # Verificar si la pregunta ya existe por texto
        cursor.execute('SELECT COUNT(*) FROM preguntas WHERE texto = %s', (texto,))
        existe = cursor.fetchone()[0]

        if existe == 0:
            cursor.execute('INSERT INTO preguntas (idP, texto) VALUES (%s, %s)', (idP, texto))
            print(f"Pregunta con ID {idP} insertada correctamente.")
        else:
            print(f"Pregunta con texto '{texto}' ya existe. Saltando inserción.")

    conn.commit()
    conn.close()
    print("Preguntas nuevas insertadas correctamente.")

# Ejecutar la función si el archivo se ejecuta directamente
if __name__ == '__main__':
    insertar_preguntas()
