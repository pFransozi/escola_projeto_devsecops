from flask import request, g, jsonify
from app.models.user import User

def autenticacao():

    #preflight request 
    if request.method == "OPTIONS":
        return '', 200
    
    if request.path in ["/api/login", "/api/usuario", "/ping-db"]:
        return
    
    user_id = request.headers.get("X-User-Id")
    if user_id:
        user = User.query.filter_by(id=user_id).first()
        if user:
            g.user = user
            return
        
    return jsonify({"error":"não autorizado"}), 401