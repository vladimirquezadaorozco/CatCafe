from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3



app = Flask(__name__)
CORS(app)  # Aplica CORS a todas las rutas y métodos

#RUTA PARA EL REGISTER DEL ADMINISTRADOR
@app.route('/register', methods=["POST"])
def register_admin():
    data = request.get_json()  # Asumiendo que los datos se envían como JSON
    username = data['username']
    password = data['password']

    # Conectar a la base de datos y crear una nueva entrada en la tabla admins
    con = sqlite3.connect("catcafeserver/catcafe.db")
    cur = con.cursor()

    # Aquí debes incluir la lógica para verificar que el usuario no exista ya,
    # y aplicar hashing a la contraseña (no almacenarla en texto plano)
    # Para este ejemplo, se omiten esas prácticas por simplicidad
    try:
        cur.execute("INSERT INTO admins (user, password) VALUES (?, ?)", (username, password))
        con.commit()
        return jsonify(message="User registered successfully"), 201
    except sqlite3.IntegrityError:
        return jsonify(message="User already exists"), 409
    finally:
        cur.close()
        con.close()
    
    
#RUTA PARA EL LOGIN DEL ADMINISTRADOR
@app.route('/login', methods=["POST"])
def login_admin():
    data = request.get_json()  # Asumiendo que los datos se envían como JSON
    username = data['username']
    password = data['password']

    # Conectar a la base de datos para verificar las credenciales en la tabla admins
    con = sqlite3.connect("catcafeserver/catcafe.db")
    con.row_factory = sqlite3.Row  # Facilita el acceso a las columnas por nombre
    cur = con.cursor()

    # Verificar si existe un registro con el username y password proporcionados
    cur.execute("SELECT * FROM admins WHERE user = ? AND password = ?", (username, password))
    admin = cur.fetchone()

    cur.close()
    con.close()

    if admin:
        # Si se encontró un registro, las credenciales son correctas
        return jsonify(message="Login successful"), 200
    else:
        # Si no se encontró un registro, las credenciales son incorrectas
        return jsonify(message="Invalid username or password"), 401


# @app.route('/getTables', methods=["GET"])
# def loginAdmin():
#     con = sqlite3.connect("catcafe.db")
#     cur = con.cursor()
#     res = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     table_names = res.fetchall()  # Obtiene todos los nombres de las tablas
#     return jsonify(table_names), 200



#RUTA PARA OBTENER LOS GATOS DE LA BASE DE DATOS
@app.route('/gatos')
def get_gatos():
    # Conectar a la base de datos
    con = sqlite3.connect("catcafeserver/catcafe.db")
    con.row_factory = sqlite3.Row  # Esto permite acceder a las columnas por nombre.
    cur = con.cursor()

    # Ejecutar la consulta para obtener los ID y nombres de los gatos
    cur.execute("SELECT id_gato, name FROM gatos")
    gatos = cur.fetchall()

    # Convertir los resultados en una lista de diccionarios
    gatos_list = [{'id_gato': gato['id_gato'], 'name': gato['name']} for gato in gatos]

    # Cerrar la conexión a la base de datos
    cur.close()
    con.close()

    # Devolver los resultados en formato JSON
    return jsonify(gatos_list)


#CON ESTA RUTA ACCEDEMOS A LA INFORMACION DE UN GATO CON CIERTO ID
@app.route('/gatos/<int:id_gato>')
def get_cat_info(id_gato):
    con = sqlite3.connect("catcafeserver/catcafe.db")
    con.row_factory = sqlite3.Row  # Facilita el acceso a las columnas por nombre
    cur = con.cursor()
    cur.execute("SELECT * FROM gatos WHERE id_gato = ?", (id_gato,))
    gato = cur.fetchone()
    cur.close()
    con.close()

    if gato:
        gato_info = {
            'id': gato["id_gato"],
            'name': gato["name"],
            'age': gato["age"],
            'race': gato["race"],
            'info': gato["info"]
        }
        return jsonify(gato_info)
    else:
        return jsonify({'message': 'Gato no encontrado'}), 404


#RUTA PARA MANDAR EL JSON DE LA SOLICITUD DE ADOPCION A LA VISTA ADMINISTRADOR
@app.route('/enviar_solicitud', methods=["POST"])
def enviar_solicitud():
    data = request.get_json()  # Aquí recibes el JSON enviado desde el cliente
    # Extrae la información del cliente y del gato del JSON recibido
    id_gato = data.get('catId')
    nombre_cliente = data.get('clienteNombre')
    email_cliente = data.get('clienteEmail')

    # Conectar a la base de datos
    con = sqlite3.connect("catcafeserver/catcafe.db")
    cur = con.cursor()

    # Insertar la nueva solicitud en la tabla de solicitudes
    try:
        cur.execute("INSERT INTO solicitudes (id_gato, name, email) VALUES (?, ?, ?)", 
                    (id_gato, nombre_cliente, email_cliente))
        con.commit()
        mensaje = 'Solicitud enviada con éxito'
        status_code = 200
    except sqlite3.IntegrityError as e:
        mensaje = 'Error al enviar la solicitud'
        status_code = 500
        print(e)

    # Cerrar la conexión a la base de datos
    cur.close()
    con.close()

    # Devolver una respuesta
    return jsonify({'message': mensaje}), status_code


@app.route('/obtener_notificaciones', methods=["GET"])
def obtener_notificaciones():
    con = sqlite3.connect("catcafeserver/catcafe.db")
    con.row_factory = sqlite3.Row  # Esto permite acceder a las columnas por nombre
    cur = con.cursor()

    # Ejecuta una consulta para obtener las últimas solicitudes
    cur.execute("SELECT * FROM solicitudes")
    solicitudes = cur.fetchall()

    # Convertir los resultados en una lista de diccionarios
    lista_solicitudes = []
    for solicitud in solicitudes:
        lista_solicitudes.append({
            'id_solicitud': solicitud['id_solicitud'],
            'id_gato': solicitud['id_gato'],
            'nombre_cliente': solicitud['name'],
            'email_cliente': solicitud['email']
        })

    cur.close()
    con.close()

    # Devuelve los resultados en formato JSON
    return jsonify(lista_solicitudes)


if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ejecutamos la aplicación Flask en modo de depuración