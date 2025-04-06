-- Criação dos schemas
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS bronze;
CREATE SCHEMA IF NOT EXISTS silver;
CREATE SCHEMA IF NOT EXISTS gold;

-- Tabelas da camada Raw (Bronze)
CREATE TABLE IF NOT EXISTS raw.users (
    _id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.customers (
    _id TEXT PRIMARY KEY,
    fantasy_name TEXT,
    cnpj TEXT,
    status TEXT,
    segment TEXT,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS raw.transactions (
    _id TEXT PRIMARY KEY,
    tenantId TEXT,
    userId TEXT,
    createdAt TIMESTAMP,
    updatedAt TIMESTAMP,
    favoriteFruit TEXT,
    isFraud BOOLEAN,
    document JSONB,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabelas da camada Bronze (Silver)
CREATE TABLE IF NOT EXISTS bronze.users (
    _id TEXT PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    ingestion_timestamp TIMESTAMP,
    validation_status TEXT,
    validation_errors JSONB
);

CREATE TABLE IF NOT EXISTS bronze.customers (
    _id TEXT PRIMARY KEY,
    fantasy_name TEXT,
    cnpj TEXT,
    status TEXT,
    segment TEXT,
    ingestion_timestamp TIMESTAMP,
    validation_status TEXT,
    validation_errors JSONB
);

CREATE TABLE IF NOT EXISTS bronze.transactions (
    _id TEXT PRIMARY KEY,
    tenantId TEXT,
    userId TEXT,
    createdAt TIMESTAMP,
    updatedAt TIMESTAMP,
    favoriteFruit TEXT,
    isFraud BOOLEAN,
    document_type TEXT,
    document_uf TEXT,
    ingestion_timestamp TIMESTAMP,
    validation_status TEXT,
    validation_errors JSONB
);

-- Views da camada Silver (Gold)
CREATE OR REPLACE VIEW silver.user_analytics AS
SELECT 
    u._id,
    u.name,
    u.email,
    c.fantasy_name as company_name,
    c.segment as company_segment,
    COUNT(t._id) as total_transactions,
    SUM(CASE WHEN t.isFraud THEN 1 ELSE 0 END) as fraud_transactions,
    COUNT(DISTINCT t.favoriteFruit) as unique_fruits
FROM bronze.users u
LEFT JOIN bronze.transactions t ON u._id = t.userId
LEFT JOIN bronze.customers c ON t.tenantId = c._id
GROUP BY u._id, u.name, u.email, c.fantasy_name, c.segment;

CREATE OR REPLACE VIEW silver.transaction_analytics AS
SELECT 
    t._id,
    t.createdAt,
    t.updatedAt,
    t.isFraud,
    t.document_type,
    t.document_uf,
    u.name as user_name,
    c.fantasy_name as company_name,
    c.segment as company_segment
FROM bronze.transactions t
LEFT JOIN bronze.users u ON t.userId = u._id
LEFT JOIN bronze.customers c ON t.tenantId = c._id;

-- Views Materializadas da camada Gold
CREATE MATERIALIZED VIEW IF NOT EXISTS gold.fraud_analysis AS
SELECT 
    DATE_TRUNC('day', t.createdAt) as transaction_date,
    c.segment as company_segment,
    t.document_type,
    t.document_uf,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN t.isFraud THEN 1 ELSE 0 END) as fraud_count,
    ROUND(AVG(CASE WHEN t.isFraud THEN 1 ELSE 0 END) * 100, 2) as fraud_percentage
FROM bronze.transactions t
JOIN bronze.customers c ON t.tenantId = c._id
GROUP BY transaction_date, c.segment, t.document_type, t.document_uf;

CREATE MATERIALIZED VIEW IF NOT EXISTS gold.user_behavior AS
SELECT 
    u._id as user_id,
    u.name as user_name,
    c.segment as company_segment,
    COUNT(DISTINCT t.favoriteFruit) as unique_fruits,
    COUNT(t._id) as total_transactions,
    MIN(t.createdAt) as first_transaction,
    MAX(t.createdAt) as last_transaction
FROM bronze.users u
LEFT JOIN bronze.transactions t ON u._id = t.userId
LEFT JOIN bronze.customers c ON t.tenantId = c._id
GROUP BY u._id, u.name, c.segment;

-- Índices para otimização
CREATE INDEX IF NOT EXISTS idx_raw_transactions_createdat ON raw.transactions(createdAt);
CREATE INDEX IF NOT EXISTS idx_bronze_transactions_createdat ON bronze.transactions(createdAt);
CREATE INDEX IF NOT EXISTS idx_bronze_transactions_userid ON bronze.transactions(userId);
CREATE INDEX IF NOT EXISTS idx_bronze_transactions_tenantid ON bronze.transactions(tenantId);

-- Função para atualizar as views materializadas
CREATE OR REPLACE FUNCTION refresh_gold_views()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW gold.fraud_analysis;
    REFRESH MATERIALIZED VIEW gold.user_behavior;
END;
$$ LANGUAGE plpgsql; 