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


# OBTENER LOS PRODUCTOS DE LA BASE DE DATOS
@app.route('/productos')
def get_productos():
        # Conectar a la base de datos
    con = sqlite3.connect("catcafeserver/catcafe.db")
    con.row_factory = sqlite3.Row  # Esto permite acceder a las columnas por nombre.
    cur = con.cursor()
    
    cur.execute("SELECT id_producto, nombre, precio from productos")
    productos = cur.fetchall()
    
    #convertir los resultados en una lista de diccionarios
    productos_list= [{'id_producto': producto['id_producto'], 'nombre': producto['nombre'], 'precio':producto['precio']} for producto in productos]

    # Cerrar la conexión a la base de datos
    cur.close()
    con.close()

    # Devolver los resultados en formato JSON
    return jsonify(productos_list)


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


# Ruta para actualizar los datos del gato conforme su id_gato
@app.route('/gatos/<int:id_gato>', methods=["PUT"])
def update_cat(id_gato):
    data = request.get_json()
    con = sqlite3.connect("catcafeserver/catcafe.db")
    cur = con.cursor()

    try:
        cur.execute("""
            UPDATE gatos 
            SET name = ?, age = ?, race = ?, info = ? 
            WHERE id_gato = ?""",
            (data['name'], data['age'], data['race'], data['info'], id_gato)
        )
        con.commit()
        if cur.rowcount == 0:
            return jsonify(message="Gato no encontrado o datos no cambiaron"), 404
        else:
            return jsonify(message="Gato actualizado con éxito"), 200
    except sqlite3.IntegrityError as e:
        print(e)
        return jsonify(message="Error al actualizar el gato"), 500
    finally:
        cur.close()
        con.close()


# Ruta para actualizar la información de un producto conforme su id_producto
@app.route('/productos/<int:id_producto>', methods=["PUT"])
def update_product(id_producto):
    data = request.get_json()
    con = sqlite3.connect("catcafeserver/catcafe.db")
    cur = con.cursor()

    try:
        cur.execute("""
            UPDATE productos 
            SET nombre = ?, disponibilidad = ?, precio = ? 
            WHERE id_producto = ?""",
            (data['nombre'], data['disponibilidad'], data['precio'], id_producto)
        )
        con.commit()
        if cur.rowcount == 0:
            return jsonify(message="Producto no encontrado o datos no cambiaron"), 404
        else:
            return jsonify(message="Producto actualizado con éxito"), 200
    except sqlite3.IntegrityError as e:
        print(e)
        return jsonify(message="Error al actualizar el producto"), 500
    finally:
        cur.close()
        con.close()




# Ruta para agregar un nuevo gato
@app.route('/gatos', methods=["POST"])
def add_cat():
    data = request.get_json()
    con = sqlite3.connect("catcafeserver/catcafe.db")
    cur = con.cursor()

    try:
        cur.execute("""
            INSERT INTO gatos (name, age, race, info) 
            VALUES (?, ?, ?, ?)""",
            (data['name'], data['age'], data['race'], data['info'])
        )
        con.commit()
        return jsonify(message="Gato agregado con éxito, recuerda agregar una imagen dentro de la base de datos"), 201
    except sqlite3.IntegrityError as e:
        print(e)
        return jsonify(message="Error al agregar el gato"), 500
    finally:
        cur.close()
        con.close()

# Ruta para agregar un nuevo producto
@app.route('/productos', methods=["POST"])
def add_product():
    data = request.get_json()
    con = sqlite3.connect("catcafeserver/catcafe.db")
    cur = con.cursor()

    try:
        cur.execute("""
            INSERT INTO productos (nombre, disponibilidad, precio) 
            VALUES (?, ?, ?)""",
            (data['nombre'], data['disponibilidad'], data['precio'])
        )
        con.commit()
        return jsonify(message="Producto agregado con éxito, recuerda agregar una imagen dentro de la base de datos"), 201
    except sqlite3.IntegrityError as e:
        print(e)
        return jsonify(message="Error al agregar el producto"), 500
    finally:
        cur.close()
        con.close()



if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ejecutamos la aplicación Flask en modo de depuración