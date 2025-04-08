import logging
from typing import Dict
from datetime import datetime

import pandas as pd
from zoneinfo import ZoneInfo

from ..storage.parquet_storage import ParquetStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataTransformer:
    def __init__(self):
        self.metrics = {}
        self.storage = ParquetStorage(base_path="data/parquet/silver")

    def transform_users(self, users_df: pd.DataFrame) -> pd.DataFrame:
        """Transforma dados de usuários"""
        logger.info("Transformando dados de usuários")
        try:
            # Primeiro renomeia todas as colunas para minúsculas
            users_df = users_df.rename(columns={
                'createdAt': 'createdat',
                'birthdate': 'birthdate',
                'name': 'name',
                'email': 'email',
                '_id': '_id'
            })
            
            # Converte timestamps para datetime de forma robusta
            users_df['createdat'] = pd.to_datetime(users_df['createdat'], utc=True)
            users_df['birthdate'] = pd.to_datetime(users_df['birthdate'], utc=True)
            
            # Ajusta para o fuso horário de Moscow
            users_df['createdat'] = users_df['createdat'].dt.tz_convert('Europe/Moscow')
            users_df['birthdate'] = users_df['birthdate'].dt.tz_convert('Europe/Moscow')
            
            # Formata as datas para string
            users_df['createdat'] = users_df['createdat'].dt.strftime('%Y-%m-%d %H:%M:%S')
            users_df['birthdate'] = users_df['birthdate'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            # Calcula idade
            now = datetime.now(ZoneInfo('Europe/Moscow'))
            birthdate_dt = pd.to_datetime(users_df['birthdate']).dt.tz_localize('Europe/Moscow')
            users_df['age'] = (now - birthdate_dt).dt.days // 365
            
            return users_df
        except Exception as e:
            logger.error(f"Erro ao transformar dados de usuários: {str(e)}")
            raise

    def transform_customers(self, customers_df: pd.DataFrame) -> pd.DataFrame:
        """Transforma dados de clientes"""
        logger.info("Transformando dados de clientes")
        try:
            # Primeiro renomeia todas as colunas para minúsculas
            customers_df = customers_df.rename(columns={
                'fantasyName': 'fantasyname',
                'cnpj': 'cnpj',
                'status': 'status',
                'segment': 'segment',
                '_id': '_id'
            })
            
            # Formata CNPJ
            customers_df['cnpj'] = customers_df['cnpj'].astype(str).str.zfill(14)
            customers_df['cnpj'] = customers_df['cnpj'].apply(
                lambda x: f"{x[:2]}.{x[2:5]}.{x[5:8]}/{x[8:12]}-{x[12:]}"
            )
            
            # Adiciona categoria de segmento baseada no segmento
            segment_categories = {
                'Banco': 'Financeiro',
                'Ecommerce': 'Varejo',
                'Serviços': 'Serviços'
            }
            customers_df['segment_category'] = customers_df['segment'].map(segment_categories)
            
            # Garante que não há valores nulos em segment_category
            if customers_df['segment_category'].isnull().any():
                logger.warning("Encontrados valores nulos em segment_category, preenchendo com 'Outros'")
                customers_df['segment_category'] = customers_df['segment_category'].fillna('Outros')
            
            return customers_df
        except Exception as e:
            logger.error(f"Erro ao transformar dados de clientes: {str(e)}")
            raise

    def transform_transactions(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Transforma dados de transações"""
        logger.info("Transformando dados de transações")
        try:
            # Primeiro renomeia todas as colunas para minúsculas
            transactions_df = transactions_df.rename(columns={
                'createdAt': 'createdat',
                'updatedAt': 'updatedat',
                'tenantId': 'tenantid',
                'userId': 'userid',
                'favoriteFruit': 'favoritefruit',
                'isFraud': 'isfraud',
                '_id': '_id'
            })
            
            # Extrai informações do documento
            transactions_df['document_type'] = transactions_df['document'].apply(lambda x: x.get('documentType', ''))
            transactions_df['document_uf'] = transactions_df['document'].apply(lambda x: x.get('documentUF', ''))
            
            # Remove a coluna document original
            transactions_df = transactions_df.drop(columns=['document'])
            
            # Converte timestamps para datetime e ajusta para UTC-3
            transactions_df['createdat'] = pd.to_datetime(transactions_df['createdat']).dt.tz_convert('Europe/Moscow')
            transactions_df['updatedat'] = pd.to_datetime(transactions_df['updatedat']).dt.tz_convert('Europe/Moscow')
            
            # Formata as datas para string
            transactions_df['createdat'] = transactions_df['createdat'].dt.strftime('%Y-%m-%d %H:%M:%S')
            transactions_df['updatedat'] = transactions_df['updatedat'].dt.strftime('%Y-%m-%d %H:%M:%S')
            
            return transactions_df
        except Exception as e:
            logger.error(f"Erro ao transformar dados de transações: {str(e)}")
            raise

    def transform_all(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Transforma todos os dados"""
        logger.info("Iniciando transformação de todos os dados")
        transformed_data = {}

        try:
            transformed_data['users'] = self.transform_users(data['users'])
            transformed_data['customers'] = self.transform_customers(data['customers'])
            transformed_data['transactions'] = self.transform_transactions(data['transactions'])

            # Salva dados transformados na camada silver
            self.storage.save_to_parquet(transformed_data)

            logger.info("Transformação de todos os dados concluída")
            return transformed_data

        except Exception as e:
            logger.error(f"Erro na transformação geral: {str(e)}")
            raise
