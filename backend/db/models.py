CREATE_USERS = """
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY,
    username VARCHAR(255),
    first_name VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

CREATE_CHANNELS = """
CREATE TABLE IF NOT EXISTS channels (
    id BIGINT PRIMARY KEY,
    owner_id BIGINT REFERENCES users(id),
    username VARCHAR(255),
    title VARCHAR(255),
    language VARCHAR(10),
    tags TEXT[],
    setup_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""
