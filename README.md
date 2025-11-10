# 🎓 SistemaEscola-API

API Restful para um sistema escolar, construída utilizando uma arquitetura de microsserviços com Python e Docker.

Colaboradores do projeto:

Ana Olivia Geraldo - RA:2403901
Gabrielle Ribeiro de Pádua - RA:2403656
Nathalia Ferreira - RA:2402413
Pedro Felipe - RA:2400450
---

## 🏛️ Arquitetura e Ecossistema de Microsserviços

O projeto é dividido em três serviços independentes, cada um rodando em seu próprio container Docker, orquestrados pelo `docker-compose.yml`.

A arquitetura é baseada em um serviço central (`gerenciamento`) do qual os outros serviços dependem para obter informações.



### Serviços
* **`gerenciamento` (Porta: 5000)**
    * **Descrição:** Serviço central da aplicação. Responsável pelo gerenciamento de entidades principais (como alunos, professores, etc.).
    * **Build:** Construído a partir do diretório `./Gerenciamento`.

* **`reservas` (Porta: 5001)**
    * **Descrição:** Serviço responsável pela lógica de reservas (ex: salas, equipamentos).
    * **Build:** Construído a partir do diretório `./Reservas`.
    * **Integração:** Este serviço **depende** do serviço `gerenciamento` para funcionar.

* **`atividades` (Porta: 5002)**
    * **Descrição:** Serviço responsável pela lógica de atividades e notas.
    * **Build:** Construído a partir do diretório `./Atividades`.
    * **Integração:** Este serviço também **depende** do serviço `gerenciamento`.

### 🔄 Fluxo de Integração entre Serviços

A comunicação entre os serviços é gerenciada pela rede interna do Docker:

1.  **Ordem de Inicialização:** O `docker-compose.yml` usa a diretiva `depends_on` para garantir que o serviço `gerenciamento` seja iniciado *antes* dos serviços `reservas` e `atividades`.
2.  **Descoberta de Serviço (Service Discovery):**
    * Os serviços `reservas` e `atividades` recebem uma variável de ambiente chamada `GERENCIAMENTO_URL` (configurada no `docker-compose.yml`).
    * O valor dessa variável é `http://gerenciamento:5000`.
    * Dentro do ambiente Docker, `gerenciamento` é resolvido como o endereço IP interno do container `gerenciamento`, permitindo que os serviços `reservas` e `atividades` façam requisições HTTP para o serviço central.

---

## 🐳 Execução com Docker

O projeto é 100% containerizado. A única dependência para execução é o **Docker** e o **Docker Compose**.

### 1. Clonar o Repositório
```bash
git clone [https://github.com/nathaliafdsousa/SistemaEscola-API.git](https://github.com/nathaliafdsousa/SistemaEscola-API.git)
cd SistemaEscola-API
