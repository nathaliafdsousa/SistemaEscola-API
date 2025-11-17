FROM python:3.11-slim

WORKDIR /app

# Copia TUDO do serviço (Models, Controller, config.py, instance, etc)
COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "run.py"]
