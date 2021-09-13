
import aiohttp
class QuickRequests():

    @classmethod
    async def get(self, url: str, headers=dict):
        connector = aiohttp.TCPConnector(limit=50, force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=headers) as resp:
                result = await resp.text()
                await resp.release()
                return result

    @classmethod
    async def get_header(self, url: str, headers=dict):
        connector = aiohttp.TCPConnector(limit=50, force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            try:
                async with session.get(url, headers=headers) as resp:
                        result = resp.headers.get('content-type')
                        await resp.release()
                        return result
            except aiohttp.ClientResponseError:
                return None
            except aiohttp.ClientConnectionError:
                pass
            except aiohttp.ClientError:
                pass