FROM python:3.11-slim

WORKDIR /app

# Copia TUDO necessário para o container (pastas, config.py, etc)
COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Porta correta (5002, mesma do docker-compose)
EXPOSE 5002

CMD ["python", "run.py"]

