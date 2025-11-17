FROM python:3.11-slim

# Diretório base
WORKDIR /app

# Copia TUDO da pasta do microserviço para /app/gerenciamento
COPY . /app/gerenciamento

# Instala dependências usando o requirements do serviço
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/gerenciamento/requirements.txt

# Porta do Flask desse serviço
EXPOSE 5000

# Roda o run.py como módulo do pacote "gerenciamento"
CMD ["python", "-m", "gerenciamento.run"]
