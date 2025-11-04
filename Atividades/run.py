from flask import Flask
from flasgger import Swagger
from config import db, migrate, swagger
from Controller.atividade_controller import atividade_bp
from Controller.nota_controller import notatividade_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///atividade.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notatividade.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    app.register_blueprint(atividade_bp)
    app.register_blueprint(notatividade_bp)

    with app.app_context():
        db.create_all()

    return app
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True,port=5001)
