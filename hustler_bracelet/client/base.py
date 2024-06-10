
from aiohttp import ClientSession


class APIHttpClient:
    async def request(self, method: str, url: str, data: dict, **kwargs):
        async with ClientSession() as session:
            async with session.request(method, url, json=data, **kwargs) as response:
                # response.raise_for_status()
                if 200 <= response.status < 300:
                    return await response.json()
