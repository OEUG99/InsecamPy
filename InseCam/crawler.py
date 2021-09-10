from random import randrange

import requests
from bs4 import BeautifulSoup
import lxml

default_header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                                'like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

class Crawler():

    def __init__(self, header=None):
        """Initialization for the wrapper.

        :param header: Optional. Provide a custom header dictionary.
        :raise Exception: Provided headers must be of dict type.
        """

        if isinstance(header, dict):
            self.header = header
        elif header is None:
            self.header = default_header
        else:
            raise Exception("[ICC] Header must be a dict.")



    async def fetch_random_cam(self):
        random_page = randrange(1000)
        random_cam = randrange(1, 6)

        URL = f"http://www.insecam.org/en/bynew/?page={random_page}"

        # Fetching the HTML from the site:
        results = requests.get(URL, headers=self.header, timeout=5)
        src = results.content

        # Sending HTML to BS to parse:
        soup = BeautifulSoup(src, 'lxml')

        tag = soup.find_all("img")[random_cam]
        tag = tag.get("src")

        return tag
