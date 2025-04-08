import logging
from datetime import datetime
from typing import Any, Dict, List

import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataQualityValidator:
    def __init__(self):
        self.validations = []

    def validate_null_values(self, df: pd.DataFrame, entity: str) -> Dict[str, Any]:
        """Valida valores nulos em um DataFrame"""
        null_counts = df.isnull().sum()
        total_rows = len(df)

        validation = {
            'entity': entity,
            'validation_type': 'null_values',
            'total_rows': total_rows,
            'null_counts': null_counts.to_dict(),
            'null_percentages': (null_counts / total_rows * 100).to_dict(),
            'timestamp': datetime.now().isoformat()
        }

        self.validations.append(validation)
        return validation

    def validate_unique_values(self, df: pd.DataFrame, entity: str, unique_columns: List[str]) -> Dict[str, Any]:
        """Valida valores únicos em colunas específicas"""
        validation = {
            'entity': entity,
            'validation_type': 'unique_values',
            'timestamp': datetime.now().isoformat()
        }

        for col in unique_columns:
            actual_col = 'id' if col == '_id' else col
            if actual_col not in df.columns:
                logger.warning(f"Coluna {actual_col} não encontrada no DataFrame")
                continue
                
            unique_count = df[actual_col].nunique()
            total_count = len(df)
            validation[col] = {
                'unique_count': unique_count,
                'total_count': total_count,
                'duplicate_percentage': ((total_count - unique_count) / total_count * 100) if total_count > 0 else 0
            }

        self.validations.append(validation)
        return validation

    def validate_data_types(self, df: pd.DataFrame, entity: str, expected_types: Dict[str, str]) -> Dict[str, Any]:
        """Valida tipos de dados das colunas"""
        actual_types = df.dtypes.astype(str).to_dict()

        validation = {
            'entity': entity,
            'validation_type': 'data_types',
            'expected_types': expected_types,
            'actual_types': actual_types,
            'timestamp': datetime.now().isoformat()
        }

        self.validations.append(validation)
        return validation

    def get_all_validations(self) -> List[Dict[str, Any]]:
        """Retorna todas as validações realizadas"""
        return self.validations
