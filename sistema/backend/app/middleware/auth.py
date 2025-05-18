from flask import request, g, jsonify
from app.models.usuario import Usuario

def autenticacao():

    #preflight request 
    if request.method == "OPTIONS":
        return '', 200
    
    if request.path in ["/api/login", "/ping-db"]:
        return
    
    user_id = request.headers.get("X-User-Id")
    if user_id:
        user = Usuario.query.filter_by(id=user_id).first()
        if user:
            g.user = user
            return
        
    return jsonify({"error":"não autorizado"}), 401