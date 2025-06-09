from app import create_app

app = create_app()

if __name__ == "__main__":
    context = ("../cert.pem", "../key.pem")
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=context)
