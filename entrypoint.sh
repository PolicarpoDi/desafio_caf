#!/bin/bash

# Cria diretórios de log e configura permissões
echo "Criando diretórios de log..."
sudo mkdir -p /opt/airflow/logs/{scheduler,webserver,dag_processor_manager}
sudo chown -R airflow:0 /opt/airflow/logs
sudo chmod -R 775 /opt/airflow/logs

# Cria diretórios de dados e configura permissões
echo "Criando diretórios de dados..."
sudo mkdir -p /opt/airflow/data/metadata
sudo chown -R airflow:0 /opt/airflow/data
sudo chmod -R 775 /opt/airflow/data

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
