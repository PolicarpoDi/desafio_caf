Vou criar um formato markdown adequado para o README:

# Pipeline de Dados - Arquitetura Medallion

## Visão Geral da Pipeline

A pipeline de dados é composta por 4 camadas principais, seguindo a arquitetura Medallion:

### 1. Extração (Raw/Bronze)
**Objetivo**: Extrair dados brutos das fontes e salvar na camada raw.

**Arquivos de entrada**:
- `data/users.json`
- `data/customers.json`
- `data/transactions.json`

**Arquivos de saída**:
- `data/parquet/raw/users_[timestamp].parquet`
- `data/parquet/raw/customers_[timestamp].parquet`
- `data/parquet/raw/transactions_[timestamp].parquet`

**Componentes**:
- `src/extractors/data_extractor.py`: Responsável por ler os arquivos JSON e converter para DataFrames
- `src/storage/parquet_storage.py`: Gerencia o armazenamento em formato Parquet

### 2. Validação (Bronze)
**Objetivo**: Validar a qualidade e estrutura dos dados.

**Arquivos de entrada**:
- Arquivos Parquet da camada raw

**Arquivos de saída**:
- `data/parquet/bronze/users_[timestamp].parquet`
- `data/parquet/bronze/customers_[timestamp].parquet`
- `data/parquet/bronze/transactions_[timestamp].parquet`

**Componentes**:
- `src/validators/data_validator.py`: Valida os dados contra schemas Pydantic
- `src/validators/data_quality.py`: Realiza validações de qualidade (nulos, duplicados, etc)
- `src/utils/schemas.py`: Define os schemas Pydantic para validação
- `src/storage/parquet_storage.py`: Gerencia o armazenamento em formato Parquet

### 3. Transformação (Silver)
**Objetivo**: Aplicar transformações e enriquecer os dados.

**Arquivos de entrada**:
- Arquivos Parquet da camada bronze

**Arquivos de saída**:
- `data/parquet/silver/users_[timestamp].parquet`
- `data/parquet/silver/customers_[timestamp].parquet`
- `data/parquet/silver/transactions_[timestamp].parquet`

**Componentes**:
- `src/transformers/data_transformer.py`: Aplica transformações nos dados
- `src/utils/schemas.py`: Define os schemas para validação pós-transformacao
- `src/storage/parquet_storage.py`: Gerencia o armazenamento em formato Parquet

### 4. Carregamento (Gold)
**Objetivo**: Carregar dados para o PostgreSQL, otimizados para consultas.

**Arquivos de entrada**:
- Arquivos Parquet da camada silver

**Arquivos de saída**:
- Tabelas no PostgreSQL:
  - `gold.users`
  - `gold.customers`
  - `gold.transactions`

**Componentes**:
- `src/loaders/gold_loader.py`: Gerencia o carregamento para o PostgreSQL
- `src/utils/schemas.py`: Define os schemas para validação final

### 5. Orquestração
**Objetivo**: Coordenar a execução da pipeline.

**Arquivos**:
- `dags/caf_pipeline.py`: Define o DAG do Airflow
- `src/utils/metadata.py`: Gerencia metadados da execução

**Configuração**:
- `docker-compose.yaml`: Configuração dos serviços
- `Dockerfile`: Configuração do container Airflow
- `entrypoint.sh`: Script de inicialização
- `requirements.txt`: Dependências Python

### 6. Metadados
**Objetivo**: Manter histórico das execuções.

**Arquivos**:
- `data/metadata/run_[uuid].json`

**Componentes**:
- `src/utils/metadata.py`: Gerencia o armazenamento e recuperação de metadados

# Validações da Camada Bronze

## 1. User
- **Validação de Email**:
  - Regex: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- **Campos Obrigatórios**:
  - `_id`
  - `name`
  - `email`
  - `createdAt`
  - `birthdate`

## 2. Customer
- **Validação de CNPJ**:
  - Verifica se tem exatamente 14 dígitos
  - Verifica se contém apenas números
- **Campos Obrigatórios**:
  - `_id`
  - `fantasyName`
  - `cnpj`
  - `status`
  - `segment`

## 3. Transaction
- **Campos Obrigatórios**:
  - `_id`
  - `tenantId`
  - `userId`
  - `createdAt`
  - `updatedAt`
  - `favoriteFruit`
  - `isFraud`
  - `document`
- **Validação de Documento**:
  - Garante que é um dicionário válido

## Processo de Validação
- Registra erros de validação para cada linha
- Mantém log de quantidade de erros
- Preserva todos os campos originais dos dados

Gostaria que eu adicionasse mais alguma informação ou detalhasse algum aspecto específico?


## Fluxo de Dados

1. Os dados são extraídos dos arquivos JSON e salvos na camada raw
2. Os dados são validados e movidos para a camada bronze
3. As transformações são aplicadas e os dados são salvos na camada silver
4. Os dados são carregados no PostgreSQL na camada gold
5. Todo o processo é orquestrado pelo Airflow
6. Metadados são gerados e armazenados em cada etapa