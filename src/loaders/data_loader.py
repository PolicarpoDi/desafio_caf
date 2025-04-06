import logging
import os
from typing import Dict

import pandas as pd
from sqlalchemy import create_engine, text

from ..utils.schemas import Customer, Transaction, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self):
        """Inicializa o DataLoader com conexão ao PostgreSQL"""
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

    def load_users(self, users_df: pd.DataFrame):
        """Carrega dados de usuários na tabela users"""
        logger.info("Carregando dados de usuários")
        try:
            # Validação pré-carregamento
            for _, row in users_df.iterrows():
                User(**row.to_dict())

            users_df.to_sql(
                'users',
                self.db_connection,
                if_exists='replace',
                index=False,
                method='multi'
            )
            logger.info("Dados de usuários carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar dados de usuários: {str(e)}")
            raise

    def load_customers(self, customers_df: pd.DataFrame):
        """Carrega dados de clientes na tabela customers"""
        logger.info("Carregando dados de clientes")
        try:
            # Validação pré-carregamento
            for _, row in customers_df.iterrows():
                Customer(**row.to_dict())

            customers_df.to_sql(
                'customers',
                self.db_connection,
                if_exists='replace',
                index=False,
                method='multi'
            )
            logger.info("Dados de clientes carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar dados de clientes: {str(e)}")
            raise

    def load_transactions(self, transactions_df: pd.DataFrame):
        """Carrega dados de transações na tabela transactions"""
        logger.info("Carregando dados de transações")
        try:
            # Validação pré-carregamento
            for _, row in transactions_df.iterrows():
                Transaction(**row.to_dict())

            transactions_df.to_sql(
                'transactions',
                self.db_connection,
                if_exists='replace',
                index=False,
                method='multi'
            )
            logger.info("Dados de transações carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar dados de transações: {str(e)}")
            raise

    def load_all(self, transformed_data: Dict[str, pd.DataFrame]):
        """Carrega todos os dados transformados"""
        logger.info("Iniciando carregamento de todos os dados")
        try:
            self.load_users(transformed_data['users'])
            self.load_customers(transformed_data['customers'])
            self.load_transactions(transformed_data['transactions'])
            logger.info("Todos os dados foram carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar todos os dados: {str(e)}")
            raise
