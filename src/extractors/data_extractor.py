import json
import logging
import os
from typing import Any, Dict, List

import boto3
import pandas as pd

from ..storage.parquet_storage import ParquetStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataExtractor:
    def __init__(self, use_s3=False):
        self.use_s3 = use_s3
        if use_s3:
            self.s3_client = boto3.client('s3')
        self.storage = ParquetStorage(base_path="data/parquet/raw")

    def read_json_file(self, file_path: str) -> pd.DataFrame:
        """Lê um arquivo JSON e retorna um DataFrame"""
        logger.info(f"Lendo arquivo: {file_path}")
        return pd.read_json(file_path)

    def extract_all(self) -> Dict[str, pd.DataFrame]:
        """Extrai todos os dados e salva na camada raw"""
        data = {}

        try:
            # Extração de usuários
            logger.info("Extraindo dados de usuários")
            users_df = self.read_json_file('data/users.json')
            data['users'] = users_df

            # Extração de clientes
            logger.info("Extraindo dados de clientes")
            customers_df = self.read_json_file('data/customers.json')
            data['customers'] = customers_df

            # Extração de transações
            logger.info("Extraindo dados de transações")
            transactions_df = self.read_json_file('data/transactions.json')
            data['transactions'] = transactions_df

            # Salva dados brutos na camada raw em Parquet
            self.storage.save_to_parquet(data)

            logger.info("Extração concluída com sucesso")
            return data

        except Exception as e:
            logger.error(f"Erro durante a extração: {str(e)}")
            raise
