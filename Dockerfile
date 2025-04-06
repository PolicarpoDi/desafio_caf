FROM apache/airflow:2.8.1-python3.11

USER root

# Instala dependências do sistema
RUN apt-get update && \
    apt-get install -y postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Cria diretórios necessários
RUN mkdir -p /opt/airflow/data/parquet/{raw,bronze,silver,gold} \
    /opt/airflow/data/metadata \
    /opt/airflow/plugins \
    /opt/airflow/dags \
    /opt/airflow/src \
    /opt/airflow/tests \
    /opt/airflow/logs/scheduler \
    /opt/airflow/logs/webserver

# Configura permissões dos diretórios
RUN chown -R airflow:0 /opt/airflow && \
    chmod -R 775 /opt/airflow && \
    find /opt/airflow -type d -exec chmod 775 {} \; && \
    find /opt/airflow -type f -exec chmod 664 {} \;

# Copia o entrypoint.sh e configura suas permissões
COPY entrypoint.sh /entrypoint.sh
RUN chown airflow:0 /entrypoint.sh && \
    chmod 775 /entrypoint.sh

# Copia requirements.txt
COPY requirements.txt /requirements.txt
RUN chown airflow:0 /requirements.txt

# Muda para usuário airflow e instala dependências Python
USER airflow
RUN pip install --user --no-cache-dir -r /requirements.txt

# Configura PYTHONPATH
ENV PYTHONPATH=/opt/airflow/src:${PYTHONPATH}

ENTRYPOINT ["/entrypoint.sh"] 