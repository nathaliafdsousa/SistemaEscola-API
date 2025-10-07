# API - Sistema de Gestão Escolar

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)

Uma API RESTful desenvolvida em Python com o framework Flask para gerenciar as operações básicas de um sistema escolar. O projeto permite o cadastro e a manipulação de dados de alunos, cursos e as matrículas que os relacionam.

Colaboradores do projeto:
   **Ana Olivia Geraldo - RA:2403901**
   **Gabrielle Ribeiro de Pádua - RA:2403656**
   **Nathalia Ferreira - RA:2402413**
   **Pedro Felipe - RA:2400450**
# Funcionalidades

A API oferece os seguintes endpoints para gerenciamento:

* **Alunos**:
    * Listar todos os alunos.
    * Buscar um aluno específico por ID.
    * Adicionar um novo aluno.
    * Atualizar os dados de um aluno.
    * Remover um aluno.
* **Cursos**:
    * Listar todos os cursos.
    * Adicionar um novo curso.
    * Remover um curso.
* **Matrículas**:
    * Listar todas as matrículas.
    * Realizar a matrícula de um aluno em um curso.

# Tecnologias Utilizadas

* **[Python](https://www.python.org/)**: Linguagem de programação principal.
* **[Flask](https://flask.palletsprojects.com/)**: Micro-framework web para a construção da API.
* **[Flask-RESTful](https://flask-restful.readthedocs.io/)**: Extensão para a criação rápida de APIs REST em Flask.
* **[Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)**: Extensão para integração com bancos de dados SQL através do ORM SQLAlchemy.
* **[SQLite](https://www.sqlite.org/)**: Banco de dados relacional utilizado no ambiente de desenvolvimento.

# Como Executar o Projeto

Siga os passos abaixo para configurar e rodar o projeto em seu ambiente local.

# Pré-requisitos

* [Python 3.8+](https://www.python.org/downloads/)
* [Git](https://git-scm.com/)

# Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/nathaliafdsousa/SistemaEscola-API.git](https://github.com/nathaliafdsousa/SistemaEscola-API.git)
    ```

2.  **Acesse o diretório do projeto:**
    ```bash
    cd SistemaEscola-API
    ```

3.  **(Recomendado) Crie e ative um ambiente virtual:**
    ```bash
    # Criar o ambiente
    python -m venv venv

    # Ativar no Windows
    .\venv\Scripts\activate

    # Ativar no Linux/macOS
    source venv/bin/activate
    ```

4.  **Instale as dependências do projeto:**
    > **Obs.**: É uma boa prática adicionar um arquivo `requirements.txt` ao projeto. Se ele não existir, você pode instalar as bibliotecas manualmente:
    ```bash
    pip install Flask Flask-RESTful Flask-SQLAlchemy
    ```

# Rodando a Aplicação

Com o ambiente configurado e as dependências instaladas, utilize o seguinte comando no terminal, a partir da raiz do projeto, para iniciar o servidor:

```bash
python -m app.run
```

A API estará disponível no endereço: `http://127.0.0.1:5000/`

---
