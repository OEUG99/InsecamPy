
import aiohttp
class QuickRequests():

    @classmethod
    async def get(self, url: str, header:dict=None, json=False):
        connector = aiohttp.TCPConnector()
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, headers=header, allow_redirects=True) as resp:
                if json is False:
                    result = await resp.text()
                elif json is True:
                    result = await resp.json()

            await resp.release()
            return result

    @classmethod
    async def get_header(self, url: str, header:dict = None):
        connector = aiohttp.TCPConnector()
        async with aiohttp.ClientSession(connector=connector) as session:
            try:
                async with session.get(url, headers=header, allow_redirects=True) as resp:
                        result = resp.headers.get('content-type')
                        await resp.release()
                        return result
            except aiohttp.ClientResponseError:
                return None
            except aiohttp.ClientConnectionError:
                print('here')
                pass
            except aiohttp.ClientError:
                pass