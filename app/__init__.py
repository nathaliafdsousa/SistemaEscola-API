#Configura a aplicação Flask; Cria a instância global do db; Inicializa extensões (SQLAlchemy, Migrate, Swagger); Retorna o app pronto para rodar

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flasgger import Swagger
from .Controllers.alunos_controller import alunos_bp 
from .Controllers.professor_controller import professores_bp
from .Controllers.turmas_controller import turmas_bp

Migrate = Migrate()
Swagger = Swagger()
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    #app config é um dicionário interno do flask onde define as configurações da aplicação

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///school.db" #pode ser que precisemos mudar o nome em caso de erro -> diz qual banco de dados será usado

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False #desliga recurso de alteração de objeto do banco de dados para não ocupar memória

    app.register_blueprint(alunos_bp)
    app.register_blueprint(professores_bp)
    app.register_blueprint(turmas_bp)
    #Permite que as rotas do controller sejam reconhecidas no principal

     #inicializa as extensões
     #passa a instância do app para cada extensão
    db.init_app(app)
    Migrate.init_app(app, db)
    Swagger.init_app(app)

    return app

__all__ = ["create_app", "db"]
db=db


