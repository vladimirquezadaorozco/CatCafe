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

#MODIFIQUE APARTIR DE AQUIIIIII

#RUTA PARA OBTENER LOS PRODUCTOS DE LA BASE DE DATOS
@app.route('/productos')
def get_productos():
    # Conectar a la base de datos
    con = sqlite3.connect("catcafeserver/catcafe.db")
    con.row_factory = sqlite3.Row  # Esto permite acceder a las columnas por nombre.
    cur = con.cursor()

    # Ejecutar la consulta para obtener los ID y nombres de los gatos
    cur.execute("SELECT id_producto, name FROM productos")
    productos = cur.fetchall()

    # Convertir los resultados en una lista de diccionarios
    productos_list = [{'id_producto': producto['id_producto'], 'name': producto['name']} for producto in productos]

    # Cerrar la conexión a la base de datos
    cur.close()
    con.close()

    # Devolver los resultados en formato JSON
    return jsonify(productos_list)

@app.route('/productos/<int:id_producto>')
def get_producto_info(id_producto):
    con = sqlite3.connect("catcafeserver/catcafe.db")
    con.row_factory = sqlite3.Row  # Facilita el acceso a las columnas por nombre
    cur = con.cursor()
    cur.execute("SELECT * FROM productos WHERE id_producto = ?", (id_producto,))
    producto = cur.fetchone()
    cur.close()
    con.close()

    if producto:
        producto_info = {
            'id': producto["id_producto"],
            'name': producto["name"],
            'disponibles': producto["disponibles"]
        }
        return jsonify(producto_info)
    else:
        return jsonify({'message': 'Producto no encontrado'}), 404

#RUTA PARA MANDAR EL JSON DEL PEDIDO A LA VISTA ADMINISTRADOR
@app.route('/enviar_pedido', methods=["POST"])
def enviar_pedido():
    data = request.get_json()  # Aquí recibes el JSON enviado desde el cliente
    # Extrae la información del cliente y del gato del JSON recibido
    id_producto  = data.get('productoID')
    nombre_cliente = data.get('clienteNombre')
    cantidad = data.get('cantidad')


    # Conectar a la base de datos
    con = sqlite3.connect("catcafeserver/catcafe.db")
    cur = con.cursor()
    
    cur.execute("SELECT costo FROM productos WHERE id_producto = ?", (id_producto,))

    # Insertar la nueva solicitud en la tabla de solicitudes
    try:
        cur.execute("INSERT INTO pedidos (id_producto, name, cantidad) VALUES (?, ?, ?)", 
                    (id_producto, nombre_cliente, cantidad))
        con.commit()
        mensaje = 'Pedido enviado con éxito'
        status_code = 200
    except sqlite3.IntegrityError as e:
        mensaje = 'Error al enviar el pedido'
        status_code = 500
        print(e)
    else:
        mensaje = "Producto no encontrado o costo no disponible"
        status_code = 404

    # Cerrar la conexión a la base de datos
    cur.close()
    con.close()

    # Devolver una respuesta
    return jsonify({'message': mensaje}), status_code

@app.route('/obtener_pedidos', methods=["GET"])
def obtener_pedidos():
    con = sqlite3.connect("catcafeserver/catcafe.db")
    con.row_factory = sqlite3.Row  # Esto permite acceder a las columnas por nombre
    cur = con.cursor()

    # Ejecuta una consulta para obtener las últimas solicitudes
    cur.execute("SELECT * FROM pedidos")
    pedidos = cur.fetchall()

    # Convertir los resultados en una lista de diccionarios
    lista_pedidos = []
    for pedido in pedidos:
        lista_pedidos.append({
            'id_pedido': pedido['id_pedido'],
            'id_producto': pedido['id_producto'],
            'nombre_cliente': pedido['name'],
            'cantidad': pedido['cantidad'],
        })

    cur.close()
    con.close()

    # Devuelve los resultados en formato JSON
    return jsonify(lista_pedidos)

#Modificar cantidad de disponibles despues de una compra
@app.route('/comprar_producto', methods=["POST"])
def comprar_producto():
    data = request.get_json()
    product_id = data.get('productId')
    cantidad_comprada = int(data.get('cantidadComprada'))

    con = sqlite3.connect("catcafeserver/catcafe.db")
    cur = con.cursor()

    try:
        # Actualizar la cantidad disponible del producto
        cur.execute("UPDATE productos SET disponibles = disponibles - ? WHERE id_producto = ? AND disponibles >= ?",
                    (cantidad_comprada, product_id, cantidad_comprada))
        if cur.rowcount == 0:
            raise ValueError("No hay suficientes productos disponibles o el producto no existe.")
        
        con.commit()
        mensaje = 'Compra realizada con éxito'
        status_code = 200
    except Exception as e:
        con.rollback()
        mensaje = str(e)
        status_code = 500
    finally:
        cur.close()
        con.close()

    return jsonify({'message': mensaje}), status_code

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    name = data['name']
    price = data['price']
    stock = data['stock']

    conn = sqlite3.connect('yourdatabase.db')
    cur = conn.cursor()
    cur.execute('INSERT INTO products (name, price, stock) VALUES (?, ?, ?)', (name, price, stock))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Producto agregado con éxito'}), 201

#HASTA ACA

if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Ejecutamos la aplicación Flask en modo de depuración