import logging
from typing import Dict, List, Any

import pandas as pd

from ..storage.parquet_storage import ParquetStorage
from ..utils.schemas import Customer, Transaction, User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataValidator:
    def __init__(self):
        self.storage = ParquetStorage(base_path="data/parquet/bronze")

    def _validate_entity(self, df: pd.DataFrame, schema_class: Any) -> pd.DataFrame:
        """Valida os dados de acordo com o esquema Pydantic"""
        validated_data: List[Dict] = []
        errors: List[Dict] = []

        for idx, row in df.iterrows():
            try:
                # Converte a linha para dicionário
                row_dict = row.to_dict()
                # Valida os dados
                validated_row = schema_class(**row_dict).dict()
                # Mantém todos os campos originais
                validated_data.append({**row_dict, **validated_row})
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

    def validate_data(self, data: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
        """Valida os dados e salva na camada bronze"""
        logger.info("Iniciando validação dos dados")
        validated_data = {}

        try:
            # Validação de usuários
            logger.info("Validando dados de usuários")
            validated_data['users'] = self._validate_entity(data['users'], User)

            # Validação de clientes
            logger.info("Validando dados de clientes")
            validated_data['customers'] = self._validate_entity(data['customers'], Customer)

            # Validação de transações
            logger.info("Validando dados de transações")
            validated_data['transactions'] = self._validate_entity(data['transactions'], Transaction)

            # Salva dados validados na camada bronze
            self.storage.save_to_parquet(validated_data)

            logger.info("Validação concluída com sucesso")
            return validated_data

        except Exception as e:
            logger.error(f"Erro durante a validação: {str(e)}")
            raise
