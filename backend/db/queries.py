import asyncpg
from db.models import CREATE_USERS, CREATE_CHANNELS

pool: asyncpg.Pool = None


async def init_pool(database_url: str):
    global pool
    pool = await asyncpg.create_pool(database_url)
    async with pool.acquire() as conn:
        await conn.execute(CREATE_USERS)
        await conn.execute(CREATE_CHANNELS)


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


async def create_channel(channel_id: int, owner_id: int, username: str | None, title: str):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO channels (id, owner_id, username, title)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (id) DO NOTHING
            """,
            channel_id, owner_id, username, title,
        )


async def get_user_channels(owner_id: int) -> list[dict]:
    async with pool.acquire() as conn:
        rows = await conn.fetch("SELECT * FROM channels WHERE owner_id = $1", owner_id)
        return [dict(r) for r in rows]


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
