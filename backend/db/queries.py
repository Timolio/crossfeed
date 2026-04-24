import asyncpg
from db.models import CREATE_USERS, CREATE_CHANNELS, ADD_MEMBER_COUNT_COLUMN, ADD_IS_ACTIVE_COLUMN

pool: asyncpg.Pool = None


async def init_pool(database_url: str):
    global pool
    pool = await asyncpg.create_pool(database_url)
    async with pool.acquire() as conn:
        await conn.execute(CREATE_USERS)
        await conn.execute(CREATE_CHANNELS)
        await conn.execute(ADD_MEMBER_COUNT_COLUMN)
        await conn.execute(ADD_IS_ACTIVE_COLUMN)


async def upsert_user(user_id: int, username: str | None, first_name: str | None):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO users (id, username, first_name)
            VALUES ($1, $2, $3)
            ON CONFLICT (id) DO NOTHING
            """,
            user_id, username, first_name,
        )


async def create_channel(channel_id: int, owner_id: int, username: str | None, title: str, member_count: int = 0):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO channels (id, owner_id, username, title, member_count, is_active)
            VALUES ($1, $2, $3, $4, $5, TRUE)
            ON CONFLICT (id) DO UPDATE SET is_active = TRUE, title = $3, username = $4, member_count = $5
            """,
            channel_id, owner_id, username, title, member_count,
        )


async def get_channel(channel_id: int) -> dict | None:
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT * FROM channels WHERE id = $1", channel_id)
        return dict(row) if row else None


async def get_user_channels(owner_id: int) -> list[dict]:
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM channels WHERE owner_id = $1 AND is_active = TRUE", owner_id)
        return [dict(r) for r in rows]


async def get_all_channels() -> list[dict]:
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT id FROM channels WHERE is_active = TRUE")
        return [dict(r) for r in rows]


async def update_member_count(channel_id: int, member_count: int):
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE channels SET member_count = $1 WHERE id = $2",
            member_count, channel_id,
        )


async def deactivate_channel(channel_id: int):
    async with pool.acquire() as conn:
        await conn.execute("UPDATE channels SET is_active = FALSE WHERE id = $1", channel_id)


async def update_channel_title(channel_id: int, title: str):
    async with pool.acquire() as conn:
        await conn.execute(
            "UPDATE channels SET title = $1 WHERE id = $2",
            title, channel_id,
        )


async def update_channel(channel_id: int, language: str, tags: list[str]):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            UPDATE channels
            SET language = $1, tags = $2, setup_complete = TRUE
            WHERE id = $3
            """,
            language, tags, channel_id,
        )
