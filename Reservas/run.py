from flask import Flask
from flasgger import Swagger
from config import db, migrate, swagger
from Controller.reserva_controller import reserva_bp

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    app.register_blueprint(reserva_bp)

    with app.app_context():
        db.create_all()

    @app.route('/')
    def home():
        return "Reservas API!"
    return app
if __name__ == '__main__':
    app=create_app()
    app.run(debug=True,port=5001)
