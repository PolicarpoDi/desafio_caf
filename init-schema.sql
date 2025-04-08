-- Criação do schema gold
CREATE SCHEMA IF NOT EXISTS gold;

-- Tabela de usuários
CREATE TABLE IF NOT EXISTS gold.users (
    _id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    birthdate TIMESTAMP NOT NULL,
    createdAt TIMESTAMP NOT NULL,
    age INTEGER NOT NULL
);

-- Tabela de clientes
CREATE TABLE IF NOT EXISTS gold.customers (
    _id VARCHAR(255) PRIMARY KEY,
    fantasyName VARCHAR(255) NOT NULL,
    cnpj VARCHAR(18) NOT NULL,
    status VARCHAR(50) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    segment_category VARCHAR(50) NOT NULL
);

-- Tabela de transações
CREATE TABLE IF NOT EXISTS gold.transactions (
    _id VARCHAR(255) PRIMARY KEY,
    tenantId VARCHAR(255) NOT NULL,
    userId VARCHAR(255) NOT NULL,
    createdAt TIMESTAMP NOT NULL,
    updatedAt TIMESTAMP NOT NULL,
    favoriteFruit VARCHAR(50) NOT NULL,
    isFraud BOOLEAN NOT NULL,
    document_type VARCHAR(50),
    document_uf VARCHAR(2),
    FOREIGN KEY (userId) REFERENCES gold.users(_id)
);

-- Views analíticas da camada Gold
CREATE OR REPLACE VIEW gold.user_analytics AS
SELECT 
    u._id,
    u.name,
    u.email,
    u.age,
    c.fantasyName as company_name,
    c.segment as company_segment,
    COUNT(t._id) as total_transactions,
    SUM(CASE WHEN t.isFraud THEN 1 ELSE 0 END) as fraud_transactions,
    COUNT(DISTINCT t.favoriteFruit) as unique_fruits
FROM gold.users u
LEFT JOIN gold.transactions t ON u._id = t.userId
LEFT JOIN gold.customers c ON t.tenantId = c._id
GROUP BY u._id, u.name, u.email, u.age, c.fantasyName, c.segment;

CREATE OR REPLACE VIEW gold.transaction_analytics AS
SELECT 
    t._id,
    t.createdAt,
    t.updatedAt,
    t.isFraud,
    t.document_type,
    t.document_uf,
    u.name as user_name,
    u.email as user_email,
    c.fantasyName as company_name,
    c.segment as company_segment
FROM gold.transactions t
LEFT JOIN gold.users u ON t.userId = u._id
LEFT JOIN gold.customers c ON t.tenantId = c._id;

-- Materialized Views para análises mais complexas
CREATE MATERIALIZED VIEW IF NOT EXISTS gold.fraud_analysis AS
SELECT 
    t.document_type,
    t.document_uf,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN t.isFraud THEN 1 ELSE 0 END) as fraud_count,
    ROUND(AVG(CASE WHEN t.isFraud THEN 1 ELSE 0 END) * 100, 2) as fraud_percentage
FROM gold.transactions t
GROUP BY t.document_type, t.document_uf;

CREATE MATERIALIZED VIEW IF NOT EXISTS gold.user_behavior AS
SELECT 
    u._id,
    u.name,
    u.email,
    u.age,
    COUNT(t._id) as total_transactions,
    COUNT(DISTINCT t.favoriteFruit) as unique_fruits,
    COUNT(DISTINCT t.document_type) as unique_document_types,
    COUNT(DISTINCT t.document_uf) as unique_states
FROM gold.users u
LEFT JOIN gold.transactions t ON u._id = t.userId
GROUP BY u._id, u.name, u.email, u.age;

-- Índices
CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON gold.transactions(userId);
CREATE INDEX IF NOT EXISTS idx_transactions_tenant_id ON gold.transactions(tenantId);
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON gold.transactions(createdAt);
CREATE INDEX IF NOT EXISTS idx_users_email ON gold.users(email);
CREATE INDEX IF NOT EXISTS idx_customers_cnpj ON gold.customers(cnpj);