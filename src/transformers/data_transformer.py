import logging
from datetime import datetime
from typing import Dict

import pandas as pd

from ..utils.schemas import Customer, Transaction, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataTransformer:
    def __init__(self):
        self.metrics = {}

    def calculate_age(self, birthdate: datetime) -> int:
        """Transforma idade do usuário"""
        today = datetime.now()
        return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

    def transform_users(self, users_df: pd.DataFrame) -> pd.DataFrame:
        """Transforma os dados de usuários"""
        logger.info("Transformando dados de usuários")
        try:
            # Validação pré-transformacao
            for _, row in users_df.iterrows():
                User(**row.to_dict())

            # Transformações
            users_df['age'] = users_df['birthdate'].apply(self.calculate_age)

            # Validação pós-transformacao
            for _, row in users_df.iterrows():
                User(**row.to_dict())

            logger.info("Transformação de usuários concluída")
            return users_df

        except Exception as e:
            logger.error(f"Erro na transformação de usuários: {str(e)}")
            raise

    def transform_transactions(self, transactions_df: pd.DataFrame) -> pd.DataFrame:
        """Transforma os dados de transações"""
        logger.info("Transformando dados de transações")
        try:
            # Validação pré-transformacao
            for _, row in transactions_df.iterrows():
                Transaction(**row.to_dict())

            # Transformações
            transactions_df['document_type'] = transactions_df['document'].apply(
                lambda x: x['documentType'])
            transactions_df['document_uf'] = transactions_df['document'].apply(
                lambda x: x['documentUF'])

            # Validação pós-transformacao
            for _, row in transactions_df.iterrows():
                Transaction(**row.to_dict())

            logger.info("Transformação de transações concluída")
            return transactions_df.drop('document', axis=1)

        except Exception as e:
            logger.error(f"Erro na transformação de transações: {str(e)}")
            raise

    def transform_all(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Transforma todos os dados"""
        logger.info("Iniciando transformação de todos os dados")
        transformed_data = {}

        try:
            transformed_data['users'] = self.transform_users(data['users'])
            transformed_data['transactions'] = self.transform_transactions(
                data['transactions'])
            # Sem transformação necessária
            transformed_data['customers'] = data['customers']

            logger.info("Transformação de todos os dados concluída")
            return transformed_data

        except Exception as e:
            logger.error(f"Erro na transformação geral: {str(e)}")
            raise
