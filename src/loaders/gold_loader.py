import logging
import os
from datetime import datetime
from typing import Dict

import pandas as pd
from sqlalchemy import create_engine, text, MetaData, Table, Column, String, JSON, DateTime, Boolean, Integer
from sqlalchemy.dialects.postgresql import insert

from ..storage.parquet_storage import ParquetStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GoldLoader:
    def __init__(self):
        """Inicializa o carregador da camada gold"""
        try:
            self.engine = create_engine(
                f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@"
                f"{os.getenv('POSTGRES_HOST', 'postgres')}:{os.getenv('POSTGRES_PORT', '5432')}/"
                f"{os.getenv('POSTGRES_DB')}"
            )
            # Testa a conexão
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            logger.info("Conexão com o banco de dados estabelecida com sucesso")
        except Exception as e:
            logger.error(f"Erro ao conectar ao banco de dados: {str(e)}")
            raise

    def load_users(self, users_df: pd.DataFrame):
        """Carrega dados de usuários na camada gold"""
        logger.info("Carregando dados de usuários na camada gold")
        try:
            # Converte DataFrame para lista de dicionários
            users_data = users_df.to_dict('records')
            
            # Cria a tabela se não existir
            metadata = MetaData()
            users_table = Table(
                'users',
                metadata,
                Column('_id', String, primary_key=True),
                Column('name', String),
                Column('email', String),
                Column('birthdate', DateTime),
                Column('createdat', DateTime),
                Column('age', Integer),
                schema='gold'
            )
            metadata.create_all(self.engine)

            # Insere ou atualiza os dados
            with self.engine.begin() as conn:
                stmt = insert(users_table).values(users_data)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['_id'],
                    set_={
                        'name': stmt.excluded.name,
                        'email': stmt.excluded.email,
                        'birthdate': stmt.excluded.birthdate,
                        'createdat': stmt.excluded.createdAt,
                        'age': stmt.excluded.age
                    }
                )
                conn.execute(stmt)

            logger.info("Dados de usuários carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar dados de usuários: {str(e)}")
            raise

    def load_customers(self, customers_df: pd.DataFrame):
        """Carrega dados de clientes na camada gold"""
        logger.info("Carregando dados de clientes na camada gold")
        try:
            # Converte DataFrame para lista de dicionários
            customers_data = customers_df.to_dict('records')
            
            # Cria a tabela se não existir
            metadata = MetaData()
            customers_table = Table(
                'customers',
                metadata,
                Column('_id', String, primary_key=True),
                Column('fantasyname', String),
                Column('cnpj', String),
                Column('status', String),
                Column('segment', String),
                Column('segment_category', String),
                schema='gold'
            )
            metadata.create_all(self.engine)

            # Insere ou atualiza os dados
            with self.engine.begin() as conn:
                stmt = insert(customers_table).values(customers_data)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['_id'],
                    set_={
                        'fantasyname': stmt.excluded.fantasyname,
                        'cnpj': stmt.excluded.cnpj,
                        'status': stmt.excluded.status,
                        'segment': stmt.excluded.segment,
                        'segment_category': stmt.excluded.segment_category
                    }
                )
                conn.execute(stmt)

            logger.info("Dados de clientes carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar dados de clientes: {str(e)}")
            raise

    def load_transactions(self, transactions_df: pd.DataFrame):
        """Carrega dados de transações na camada gold"""
        logger.info("Carregando dados de transações na camada gold")
        try:
            # Converte DataFrame para lista de dicionários
            transactions_data = transactions_df.to_dict('records')
            
            # Cria a tabela se não existir
            metadata = MetaData()
            transactions_table = Table(
                'transactions',
                metadata,
                Column('_id', String, primary_key=True),
                Column('tenantid', String),
                Column('userid', String),
                Column('createdat', DateTime),
                Column('updatedat', DateTime),
                Column('favoritefruit', String),
                Column('isfraud', Boolean),
                Column('document_type', String),
                Column('document_uf', String),
                schema='gold'
            )
            metadata.create_all(self.engine)

            # Insere ou atualiza os dados
            with self.engine.begin() as conn:
                stmt = insert(transactions_table).values(transactions_data)
                stmt = stmt.on_conflict_do_update(
                    index_elements=['_id'],
                    set_={
                        'tenantid': stmt.excluded.tenantid,
                        'userid': stmt.excluded.userid,
                        'createdat': stmt.excluded.createdat,
                        'updatedat': stmt.excluded.updatedat,
                        'favoritefruit': stmt.excluded.favoritefruit,
                        'isfraud': stmt.excluded.isfraud,
                        'document_type': stmt.excluded.document_type,
                        'document_uf': stmt.excluded.document_uf
                    }
                )
                conn.execute(stmt)

            logger.info("Dados de transações carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar dados de transações: {str(e)}")
            raise

    def load_all(self, data: Dict[str, pd.DataFrame]):
        """Carrega todos os dados na camada gold"""
        try:
            self.load_users(data['users'])
            self.load_customers(data['customers'])
            self.load_transactions(data['transactions'])
            logger.info("Todos os dados carregados com sucesso")
        except Exception as e:
            logger.error(f"Erro ao carregar todos os dados: {str(e)}")
            raise 