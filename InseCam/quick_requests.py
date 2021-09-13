
import aiohttp
class QuickRequests():

    @classmethod
    async def get(self, url: str, headers=dict):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                return await resp.text()

    @classmethod
    async def get_header(self, url: str, headers=dict):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers) as resp:
                        return resp.headers.get('content-type')
            except aiohttp.ClientResponseError:
                return None