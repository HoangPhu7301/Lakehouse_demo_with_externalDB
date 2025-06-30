CREATE DATABASE hive_metastore;

CREATE USER hive WITH PASSWORD 'hive';

-- Grant all privileges on the database to the hive user
GRANT ALL PRIVILEGES ON DATABASE hive_metastore TO hive;

\c hive_metastore;

-- Grant schema privileges
GRANT ALL ON SCHEMA public TO hive;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hive;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hive;

-- Grant future privileges (for tables created later)
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO hive;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO hive;

-- Create extension for better UUID support (optional but recommended)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

SELECT 'Hive Metastore database initialized successfully' AS status;