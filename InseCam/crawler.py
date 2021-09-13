from random import randrange
import requests
from bs4 import BeautifulSoup
import lxml
import cchardet
from .camera import *
import asyncio
import concurrent.futures
from .quick_requests import *
from .errors import *



class Crawler():

    def __init__(self, header=None):

        self._allowed_manufacturers = None
        self._header = None
        self._createdProperly = None

    @classmethod
    async def create(cls, header=None):

        self = cls()

        # Checking if header is a dict before assigning to atribute.
        if isinstance(header, dict):
            self._header = header
        elif header is None:
            # If there is no header, we'll set a default one.
            self._header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, '
                                          'like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        else:
            raise InvalidArgument("[ICC] Header must be a dict.")

        self._allowed_manufacturers = await self.__fetch_manufacturers_set(header=self._header)
        self._createdProperly = True
        return self

    async def __fetch_manufacturers_set(self, header=None):
        """Fetches the set of allowed manufacteres.
        :param header: optional.
        """
        allowed_manufacturers = set()

        src = await QuickRequests.get("http://www.insecam.org/en/", header)
        soup = BeautifulSoup(src, 'lxml')

        for ul in soup.find_all("ul", {"class": "dropdown-menu"}):
            for a in ul.find_all('a'):
                allowed_manufacturers.add(a.get('title')[:-8])

        return allowed_manufacturers

    async def fetch_cam_from_url(self, URL, pageNum=None, camPosNum=None):
        # Generating random camera position if one isn't provided as argument.
        if camPosNum is None:
            camPosNum = randrange(1, 6)

        src = await QuickRequests.get(URL, self._header)

        # Sending HTML to BS to parse:
        soup = BeautifulSoup(src, 'lxml')

        # Generating random page number to pick from if a page number isn't provided as argument:
        if pageNum is None:
            # Parsing out the max page number, and cleaning up parsed result:
            try:
                raw_maxPageNum = str(soup.find("ul", {"class": "pagination"}).find("script"))
                maxPageNum = int(raw_maxPageNum[43:-20])
                # Generating random page from the max page number.
                pageNum = randrange(maxPageNum)
            except AttributeError:
                pass
        tag = soup.find_all("img")[camPosNum]
        image_url = tag.get("src")
        id = int(tag.get("id").replace("image", ''))  # Fetching InsecCam ID and converting to INT.
        # Creating a Camera object associated with the given ID, and returning it.

        cam = await Camera().create(id, image_url, self._header)
        return cam

    async def __check_manufacturers(self, name: str):
        status = False

        if name in self._allowed_manufacturers:
            status = True

        return status

    @property
    async def allowed_manufacturer(self):
        return self._allowed_manufacturers

    async def fetch_by_new(self):
        return await self.fetch_cam_from_url("http://www.insecam.org/en/bynew/")

    async def fetch_by_most_popular(self):
        return await self.fetch_cam_from_url("http://www.insecam.org/en/byrating/")

    async def fetch_by_manufacturer(self, manufacturer: str):
        if await self.__check_manufacturers(manufacturer):
            return await self.fetch_cam_from_url(f"http://www.insecam.org/en/bytype/{manufacturer}/")
        else:
            raise InvalidManufacturer("[ICC] Your manufactuerer is not one supported by Inseccam.org")
