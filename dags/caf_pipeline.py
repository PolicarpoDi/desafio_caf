import uuid
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.extractors.data_extractor import DataExtractor
from src.loaders.data_loader import DataLoader
from src.transformers.data_transformer import DataTransformer
from src.utils.metadata import PipelineMetadata
from src.validators.data_quality import DataQualityValidator
from src.validators.data_validator import DataValidator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


def extract_data():
    """Task para extrair dados brutos para a camada raw"""
    run_id = str(uuid.uuid4())
    metadata = PipelineMetadata()

    try:
        extractor = DataExtractor()
        data = extractor.extract_all()

        # Salva metadados da extração
        metadata.save_run_metadata(run_id, {
            'stage': 'extract',
            'status': 'success',
            'data_counts': {k: len(v) for k, v in data.items()}
        })

        return data, run_id
    except Exception as e:
        metadata.save_run_metadata(run_id, {
            'stage': 'extract',
            'status': 'error',
            'error': str(e)
        })
        raise


def validate_data(**context):
    """Task para validar dados e salvar na camada bronze"""
    data, run_id = context['task_instance'].xcom_pull(task_ids='extract_data')
    metadata = PipelineMetadata()
    quality_validator = DataQualityValidator()

    try:
        # Validação de schema
        validator = DataValidator()
        validated_data = validator.validate_data(data)

        # Validações de qualidade
        for entity, df in validated_data.items():
            quality_validator.validate_null_values(df, entity)
            if entity == 'users':
                quality_validator.validate_unique_values(
                    df, entity, ['_id', 'email'])
            elif entity == 'customers':
                quality_validator.validate_unique_values(
                    df, entity, ['_id', 'cnpj'])
            elif entity == 'transactions':
                quality_validator.validate_unique_values(df, entity, ['_id'])

        # Salva metadados da validação
        metadata.save_run_metadata(run_id, {
            'stage': 'validate',
            'status': 'success',
            'quality_validations': quality_validator.get_all_validations()
        })

        return validated_data, run_id
    except Exception as e:
        metadata.save_run_metadata(run_id, {
            'stage': 'validate',
            'status': 'error',
            'error': str(e)
        })
        raise


def transform_data(**context):
    """Task para transformar dados e salvar na camada silver"""
    data, run_id = context['task_instance'].xcom_pull(task_ids='validate_data')
    metadata = PipelineMetadata()

    try:
        transformer = DataTransformer()
        transformed_data = transformer.transform_all(data)

        # Salva metadados da transformação
        metadata.save_run_metadata(run_id, {
            'stage': 'transform',
            'status': 'success',
            'transformations_applied': ['age_calculation', 'document_type_extraction']
        })

        return transformed_data, run_id
    except Exception as e:
        metadata.save_run_metadata(run_id, {
            'stage': 'transform',
            'status': 'error',
            'error': str(e)
        })
        raise


def load_data(**context):
    """Task para carregar dados na camada gold"""
    data, run_id = context['task_instance'].xcom_pull(
        task_ids='transform_data')
    metadata = PipelineMetadata()

    try:
        loader = DataLoader()
        loader.load_all(data)

        # Salva metadados do carregamento
        metadata.save_run_metadata(run_id, {
            'stage': 'load',
            'status': 'success',
            'tables_loaded': ['users', 'customers', 'transactions']
        })
    except Exception as e:
        metadata.save_run_metadata(run_id, {
            'stage': 'load',
            'status': 'error',
            'error': str(e)
        })
        raise


with DAG(
    'caf_pipeline',
    default_args=default_args,
    description='Pipeline de dados da caf',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['caf', 'data_pipeline'],
) as dag:

    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    validate_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
    )

    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_data,
    )

    extract_task >> validate_task >> transform_task >> load_task
