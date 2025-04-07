import json
import logging
import os
from typing import Any, Dict, List

import boto3
import pandas as pd
from sqlalchemy import create_engine, text

from ..storage.parquet_storage import ParquetStorage
from ..utils.schemas import Customer, Transaction, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExtractor:
    def __init__(self, use_s3=False):
        self.use_s3 = use_s3
        if use_s3:
            self.s3_client = boto3.client('s3')
        self.storage = ParquetStorage(base_path="data/parquet/raw")

        # Inicializa conexão com PostgreSQL
        try:
            self.db_connection = create_engine(
                f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
                f"{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', '5432')}/"
                f"{os.getenv('POSTGRES_DB')}"
            )
            # Testa a conexão
            with self.db_connection.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info(
                "Conexão com o banco de dados estabelecida com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
            raise

    def read_json_file(self, file_path: str) -> pd.DataFrame:
        """Lê um arquivo JSON e retorna um DataFrame"""
        logger.info(f"Lendo arquivo: {file_path}")
        return pd.read_json(file_path)

    def validate_data(self, df: pd.DataFrame, schema_class: Any) -> pd.DataFrame:
        """Valida os dados de acordo com o esquema Pydantic"""
        validated_data: List[Dict] = []
        errors: List[Dict] = []

        for idx, row in df.iterrows():
            try:
                validated_data.append(schema_class(**row.to_dict()).dict())
            except Exception as e:
                errors.append({
                    'row': idx,
                    'error': str(e)
                })
                logger.warning(f"Erro na validação da linha {idx}: {str(e)}")

        if errors:
            logger.warning(f"Total de erros de validação: {len(errors)}")
            # TODO: Implementar estratégia de tratamento de erros (ex: salvar em tabela de erros)

        return pd.DataFrame(validated_data)

    def save_to_postgres(self, df: pd.DataFrame, table_name: str):
        """Salva um DataFrame no PostgreSQL"""
        logger.info(f"Salvando dados na tabela {table_name}")
        try:
            # Converte o campo document para JSONB se existir
            if 'document' in df.columns:
                df['document'] = df['document'].apply(
                    lambda x: json.dumps(x) if isinstance(x, dict) else x)

            df.to_sql(
                table_name,
                self.db_connection,
                schema='raw',
                if_exists='replace',
                index=False,
                method='multi'
            )
            logger.info(f"Dados salvos com sucesso na tabela raw.{table_name}")
        except Exception as e:
            logger.error(f"Erro ao salvar dados no PostgreSQL: {str(e)}")
            raise

    def extract_all(self) -> Dict[str, pd.DataFrame]:
        """Extrai todos os dados e salva na camada raw"""
        data = {}

        try:
            # Extração de usuários
            logger.info("Extraindo dados de usuários")
            users_df = self.read_json_file('data/users.json')
            data['users'] = users_df
            self.save_to_postgres(users_df, 'users')

            # Extração de clientes
            logger.info("Extraindo dados de clientes")
            customers_df = self.read_json_file('data/customers.json')
            data['customers'] = customers_df
            self.save_to_postgres(customers_df, 'customers')

            # Extração de transações
            logger.info("Extraindo dados de transações")
            transactions_df = self.read_json_file('data/transactions.json')
            data['transactions'] = transactions_df
            self.save_to_postgres(transactions_df, 'transactions')

            # Salva dados brutos na camada raw em Parquet
            self.storage.save_to_parquet(data)

            logger.info("Extração concluída com sucesso")
            return data

        except Exception as e:
            logger.error(f"Erro durante a extração: {str(e)}")
            raise
