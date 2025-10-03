from app import create_app

app = create_app()

if __name__ == "__main_":
    app.run(debug=True) #debug=True ativa o modo debug e reinicia o servidor automaticamente ao detectar mudanças no código