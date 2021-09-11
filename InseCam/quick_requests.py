
import aiohttp
class QuickRequests():

    @classmethod
    async def get(self, url: str, headers=dict):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                results = await resp.text()

                return results

