import logging
import os
from datetime import datetime
from typing import Dict

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParquetStorage:
    def __init__(self, base_path: str = "data/parquet"):
        """Inicializa o armazenamento Parquet"""
        self.base_path = base_path
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        """Garante que o diretório base existe"""
        os.makedirs(self.base_path, exist_ok=True)

    def get_file_path(self, entity: str) -> str:
        """Gera o caminho do arquivo Parquet"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.base_path, f"{entity}_{timestamp}.parquet")

    def save_to_parquet(self, data: Dict[str, pd.DataFrame]):
        """Salva os DataFrames em arquivos Parquet"""
        logger.info("Iniciando salvamento em Parquet")
        try:
            for entity, df in data.items():
                file_path = self.get_file_path(entity)
                df.to_parquet(file_path, index=False)
                logger.info(f"Dados de {entity} salvos em {file_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar dados em Parquet: {str(e)}")
            raise

    def read_from_parquet(self, entity: str, timestamp: str = None) -> pd.DataFrame:
        """Lê dados de um arquivo Parquet"""
        try:
            if timestamp:
                file_path = os.path.join(
                    self.base_path, f"{entity}_{timestamp}.parquet")
            else:
                # Pega o arquivo mais recente
                files = [f for f in os.listdir(
                    self.base_path) if f.startswith(f"{entity}_")]
                if not files:
                    raise FileNotFoundError(
                        f"Nenhum arquivo Parquet encontrado para {entity}")
                latest_file = max(files)
                file_path = os.path.join(self.base_path, latest_file)

            logger.info(f"Lendo dados de {file_path}")
            return pd.read_parquet(file_path)
        except Exception as e:
            logger.error(f"Erro ao ler dados do Parquet: {str(e)}")
            raise
