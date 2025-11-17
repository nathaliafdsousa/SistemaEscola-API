🎓 SistemaEscola-API

API Restful para um sistema escolar, construída utilizando uma arquitetura de microsserviços com Python e Docker.

👥 Colaboradores do projeto
	•	Ana Olivia Geraldo - RA: 2403901
	•	Gabrielle Ribeiro de Pádua - RA: 2403656
	•	Nathalia Ferreira - RA: 2402413
	•	Pedro Felipe - RA: 2400450

🏛️ Arquitetura e Ecossistema de Microsserviços

O projeto é dividido em três serviços independentes, cada um rodando em seu próprio container Docker, orquestrados pelo docker-compose.yml.

A arquitetura é baseada em um serviço central (gerenciamento) do qual os outros serviços dependem para obter informações.

📌 Serviços

gerenciamento — Porta 5000
	•	Descrição: Serviço central da aplicação. Responsável pela gestão dos dados principais.
	•	Build: Diretório ./Gerenciamento

reservas — Porta 5001
	•	Descrição: Serviço responsável pelo controle de reservas.
	•	Build: Diretório ./Reservas
	•	Depende de: gerenciamento

atividades — Porta 5002
	•	Descrição: Serviço responsável pela lógica de atividades e notas.
	•	Build: Diretório ./Atividades
	•	Depende de: gerenciamento

🔄 Fluxo de Integração entre os Serviços
	1.	Ordem de Inicialização
O docker-compose.yml utiliza depends_on garantindo que o serviço gerenciamento suba primeiro.
	2.	Service Discovery (Descoberta de Serviços)
	•	Os serviços reservas e atividades recebem a variável
GERENCIAMENTO_URL=http://gerenciamento:5000
	•	Dentro do Docker, o nome do serviço vira o endereço interno do container.

🐳 Execução com Docker

O projeto é totalmente containerizado. Você só precisa do:
	•	Docker
	•	Docker Compose (já vem no Docker Desktop)

1️⃣ Clonar o Repositório

git clone https://github.com/nathaliafdsousa/SistemaEscola-API.git
cd SistemaEscola-API

2️⃣ Rodar TUDO com Docker Compose

Dentro da pasta raiz do projeto:

▶️ Subir os containers (com build)

docker compose up --build

▶️ Subir sem rebuild

docker compose up

🛑 Parar tudo

docker compose down

🧹 Parar e remover tudo (incluindo volumes)

docker compose down -v

🖥️ Executar Manualmente pelo Terminal (sem Docker)

Se quiser rodar cada serviço individualmente, siga abaixo.

📌 1. Rodar o serviço Gerenciamento

Comando:

cd Gerenciamento
python -m gerenciamento.run

	Esse serviço roda normalmente na porta 5000.

📌 2. Rodar o serviço Reservas

Comando:

cd Reservas
python run.py

	Certifique-se de que o serviço gerenciamento esteja rodando primeiro.
Porta padrão: 5001

📌 3. Rodar o serviço Atividades

Comando:

cd Atividades
python run.py

	Porta padrão: 5002

🌐 Endpoints (Padrão)

Serviço	Porta	Exemplo de URL
Gerenciamento	5000	http://localhost:5000
Reservas	5001	http://localhost:5001
Atividades	5002	http://localhost:5002

📝 Dicas Importantes
	•	Todos os microsserviços precisam do gerenciamento ativo para funcionar.
	•	Se rodar manualmente sem Docker, configure a variável de ambiente:

GERENCIAMENTO_URL=http://localhost:5000

