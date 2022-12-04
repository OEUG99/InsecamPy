import aiohttp
class QuickRequests():

    @classmethod
    async def get(self, url: str, header:dict=None, json=False, ):
        """ Function designed for making aiohttp a bit easier, basically sends a get requests.

        :param url:
        :param header:
        :param json: Bool. Determines if the output should be in json format or not.
        :return:
        """
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
        """ Function designed for making aiohttp a bit easier, basically a way to get the content type of a header.
        Useful for checking if an image is a jpeg.

        :param url:
        :param header:
        :return:
        """
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
                pass
            except aiohttp.ClientError:
                pass