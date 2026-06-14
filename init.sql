CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    card_id VARCHAR(50) UNIQUE NOT NULL,
    user_name VARCHAR(100) NOT NULL,
    company_name VARCHAR(100),
    department VARCHAR(100)
);