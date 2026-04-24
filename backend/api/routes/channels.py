from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db import queries

router = APIRouter(prefix="/api/channels")


class ChannelUpdate(BaseModel):
    language: str
    tags: list[str]


@router.get("/{user_id}")
async def get_channels(user_id: int):
    channels = await queries.get_user_channels(user_id)
    for c in channels:
        c["id"] = str(c["id"])
        c["owner_id"] = str(c["owner_id"])
        if c.get("created_at"):
            c["created_at"] = c["created_at"].isoformat()
    return channels


@router.get("/channel/{channel_id}")
async def get_channel(channel_id: int):
    channel = await queries.get_channel(channel_id)
    if not channel:
        raise HTTPException(status_code=404)
    channel["id"] = str(channel["id"])
    channel["owner_id"] = str(channel["owner_id"])
    if channel.get("created_at"):
        channel["created_at"] = channel["created_at"].isoformat()
    return channel


@router.patch("/{channel_id}")
async def update_channel(channel_id: int, data: ChannelUpdate):
    await queries.update_channel(channel_id, data.language, data.tags)
    return {"ok": True}
