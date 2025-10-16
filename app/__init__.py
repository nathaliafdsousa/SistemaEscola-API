from flask import Flask
# Importando as extensões do config
from .config import db, migrate, swagger
from .Controllers.main_controller import main_bp
from .Controllers.alunos_controller import alunos_bp 
from .Controllers.professor_controller import professores_bp
from .Controllers.turmas_controller import turmas_bp

def create_app():
    app = Flask(__name__)
    
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db" 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False 

    app.config['SWAGGER'] = {
        'title': 'SISTEMASCOLA-API',
        'uiversion': 3,
        'APISPEC_SWAGGER_UI_URL': '/apidocs/',
        'doc_dir': app.root_path,
        'APISPEC_AUTO_SCAN': True,
        
        # CORREÇÃO CRÍTICA PARA ERROS DE 'None is not defined'
        # Isso força o Flagger a lidar com o serializador YAML corretamente.
        'APISPEC_AUTO_SCAN_ROUTES': False, # Desabilita o scan automático de rotas, usaremos Blueprints
        'APISPEC': {
            'security': [], # Garante que este campo exista
            'basePath': '/',
            'info': {'description': 'API para Gerenciamento Escolar', 'title': 'SISTEMASCOLA-API', 'version': '1.0.0'}
        }
    }
    
    # IMPORTANTE: A inicialização das extensões deve vir antes do registro dos Blueprints
    # Isso resolve o problema de "No operations defined in spec!"
    db.init_app(app)
    migrate.init_app(app, db)
     # O Flagger/Swagger é inicializado primeiro

    # Registro dos Blueprints (Agora o Swagger pode escanear as rotas corretamente)
    app.register_blueprint(main_bp)
    app.register_blueprint(alunos_bp)
    app.register_blueprint(professores_bp)
    app.register_blueprint(turmas_bp)
    
    swagger.init_app(app)
    return app

__all__ = ["create_app", "db"]
db=db
