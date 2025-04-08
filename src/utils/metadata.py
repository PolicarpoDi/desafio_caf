import json
import logging
import os
from datetime import datetime
from typing import Any, Dict
from zoneinfo import ZoneInfo

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PipelineMetadata:
    def __init__(self, base_path: str = "data/metadata"):
        self.base_path = base_path
        self.ensure_directory_exists()

    def ensure_directory_exists(self):
        """Garante que o diretório base existe"""
        os.makedirs(self.base_path, exist_ok=True)

    def get_metadata_file(self, run_id: str) -> str:
        """Gera o caminho do arquivo de metadados"""
        return os.path.join(self.base_path, f"run_{run_id}.json")

    def save_run_metadata(self, run_id: str, metadata: Dict[str, Any]):
        """Salva metadados de uma execução do pipeline"""
        try:
            # Ajusta o timestamp para o horário do Brasil
            brazil_tz = datetime.now(ZoneInfo("America/Sao_Paulo"))
            metadata['timestamp'] = brazil_tz.strftime("%d/%m/%Y %H:%M:%S")
            file_path = self.get_metadata_file(run_id)

            with open(file_path, 'w') as f:
                json.dump(metadata, f, indent=2)

            logger.info(f"Metadados salvos em {file_path}")
        except Exception as e:
            logger.error(f"Erro ao salvar metadados: {str(e)}")
            raise

    def get_run_metadata(self, run_id: str) -> Dict[str, Any]:
        """Recupera metadados de uma execução do pipeline"""
        try:
            file_path = self.get_metadata_file(run_id)
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Erro ao recuperar metadados: {str(e)}")
            raise
