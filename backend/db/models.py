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
    member_count INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    setup_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
"""

ADD_MEMBER_COUNT_COLUMN = """
ALTER TABLE channels ADD COLUMN IF NOT EXISTS member_count INTEGER DEFAULT 0;
"""

ADD_IS_ACTIVE_COLUMN = """
ALTER TABLE channels ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;
"""
