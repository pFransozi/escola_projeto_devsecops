from flask import Blueprint, jsonify
from app import db
from sqlalchemy import text

teste_db_bp = Blueprint("teste_db", __name__)

@teste_db_bp.route("/ping-db", methods=["GET"])
def ping_db():
    """Verifica a conectividade com o banco de dados executando uma consulta simples."""

    try:
        result = db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "db_response": list(result)[0][0]})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
