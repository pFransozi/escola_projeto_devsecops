from flask import Flask, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

@app.route("/api/hello")
def hello():
    try:
        connection = mysql.connector.connect(
            host="db",
            user="root",
            password="root",
            database="escola_db"
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            return jsonify(message=f"Conexão bem-sucedida com o MySQL {db_Info}")
    except Error as e:
        return jsonify(message=f"Erro ao conectar com o banco de dados: {str(e)}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
