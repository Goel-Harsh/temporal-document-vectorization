from temporalio import activity
import aiohttp
import os

SUPPORTED_TYPES = {'.docx', '.doc', '.xlsx', '.xls', '.pdf'}

@activity.defn
async def fetch_document(url: str, filetype: str):
    SUPPORTED_TYPES = {'pdf', 'docx', 'doc', 'xlsx', 'xls'}
    if filetype.lower() not in SUPPORTED_TYPES:
        raise ValueError(f"Unsupported file type: {filetype}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            content = await resp.read()
    return content
