FROM python:3.11-slim

WORKDIR /app

# Copia TUDO do serviço (Models, Controllers, config.py, etc)
COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python","-m", "app.run"]
