#!/bin/bash

# Aguarda o PostgreSQL estar pronto
until pg_isready -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Aguardando PostgreSQL..."
  sleep 2
done

# Inicializa o banco do Airflow
echo "Executando airflow db upgrade..."
airflow db upgrade

# Cria o usuário admin (ignora se já existe)
echo "Criando usuário admin do Airflow (se necessário)..."
airflow users create \
    --username airflow \
    --firstname Airflow \
    --lastname Admin \
    --role Admin \
    --email airflow@example.com \
    --password airflow || true

# Executa o comando do container (scheduler, webserver, etc)
exec "$@"
