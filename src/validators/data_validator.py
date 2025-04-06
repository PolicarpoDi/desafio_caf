import logging
from typing import Dict

import pandas as pd

from ..storage.parquet_storage import ParquetStorage
from ..utils.schemas import Customer, Transaction, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataValidator:
    def __init__(self):
        self.storage = ParquetStorage(base_path="data/parquet/bronze")

    def validate_data(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Valida os dados e salva na camada bronze"""
        logger.info("Iniciando validação dos dados")
        validated_data = {}

        try:
            # Validação de usuários
            logger.info("Validando dados de usuários")
            validated_users = []
            for _, row in data['users'].iterrows():
                validated_users.append(User(**row.to_dict()).dict())
            validated_data['users'] = pd.DataFrame(validated_users)

            # Validação de clientes
            logger.info("Validando dados de clientes")
            validated_customers = []
            for _, row in data['customers'].iterrows():
                validated_customers.append(Customer(**row.to_dict()).dict())
            validated_data['customers'] = pd.DataFrame(validated_customers)

            # Validação de transações
            logger.info("Validando dados de transações")
            validated_transactions = []
            for _, row in data['transactions'].iterrows():
                validated_transactions.append(
                    Transaction(**row.to_dict()).dict())
            validated_data['transactions'] = pd.DataFrame(
                validated_transactions)

            # Salva dados validados na camada bronze
            self.storage.save_to_parquet(validated_data)

            logger.info("Validação concluída com sucesso")
            return validated_data

        except Exception as e:
            logger.error(f"Erro durante a validação: {str(e)}")
            raise
