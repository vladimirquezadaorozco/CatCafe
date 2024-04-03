from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3




app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "*"}}) # Permitir solicitudes desde cualquier origen en cualquier ruta


#RUTA PARA EL LOGIN DEL ADMINISTRADOR
@app.route('/register', methods=["POST"])
def login_admin():
    data = request.get_json()  # Asumiendo que los datos se envían como JSON
    username = data['username']
    password = data['password']

    # Conectar a la base de datos y crear una nueva entrada en la tabla admins
    con = sqlite3.connect("catcafe.db")
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
    
    
@app.route('/login', methods=["POST"])
def login_admin():
    data = request.get_json()  # Asumiendo que los datos se envían como JSON
    username = data['username']
    password = data['password']

    # Conectar a la base de datos para verificar las credenciales en la tabla admins
    con = sqlite3.connect("catcafe.db")
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


if __name__ == '__main__':
    app.run(debug=True)  # Ejecutamos la aplicación Flask en modo de depuración