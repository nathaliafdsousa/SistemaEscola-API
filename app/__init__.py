#Configura a aplicação Flask; Cria a instância global do db; Inicializa extensões (SQLAlchemy, Migrate, Swagger); Retorna o app pronto para rodar

from flask import Flask
from .config import db, migrate, swagger
from .Controllers.main_controller import main_bp
from .Controllers.alunos_controller import alunos_bp 
from .Controllers.professor_controller import professores_bp
from .Controllers.turmas_controller import turmas_bp

def create_app():
    app = Flask(__name__)
    #app config é um dicionário interno do flask onde define as configurações da aplicação

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db" #pode ser que precisemos mudar o nome em caso de erro -> diz qual banco de dados será usado

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #desliga recurso de alteração de objeto do banco de dados para não ocupar memória

    app.register_blueprint(main_bp)
    app.register_blueprint(alunos_bp)
    app.register_blueprint(professores_bp)
    app.register_blueprint(turmas_bp)
    #Permite que as rotas do controller sejam reconhecidas no principal

     #inicializa as extensões
     #passa a instância do app para cada extensão
    db.init_app(app)
    migrate.init_app(app, db)
    swagger.init_app(app)

    return app

__all__ = ["create_app", "db"]
db=db


