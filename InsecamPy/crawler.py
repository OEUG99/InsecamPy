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
from typing import Optional

async def crawler(header: Optional[dict] = None):
    crawler = Crawler()
    crawler = await crawler.create(header)
    return crawler

class Crawler:

    @classmethod
    async def create(cls, header: Optional[dict] = None):
        """Factory method. Used to properly creating an instance of this class.

        :param header: `dict` that represants header information.
        :return: returns a `Crawler` object that is properly initalized.
        """
        self = cls()
        self._allowed_manufacturers = None
        self._allowed_countries = None
        self._allowed_places = None
        self._header = None

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
        self._allowed_countries = await self.__fetch_country_dict(header=self._header)
        self._allowed_places = await self.__fetch_places_dict(header=self._header)

        return self

    async def fetch_cam_from_url(self, URL: Optional[str],
                                 pageNum: Optional[int] = None,
                                 camPosNum: Optional[int] = None) -> Camera:
        """ Method for fetching the cameras information from a insecam url. Currently, only catagory URLs are supported.

        :param URL: insecam catagory URL. (Eg: most popular, manufactuerers, countries)
        :param pageNum:
        :param camPosNum:
        :return:
        """

        # TODO: Add functionality for fetching the camera info from an individual camera URL, not just catagories.

        # Generating random camera position if one isn't provided as argument.
        if camPosNum is None:
            camPosNum = randrange(1, 6)

        # Generating random page number to pick from if a page number isn't provided as argument:
        if pageNum is None:
            pageNum = await self.__fetch_page_num(URL)

        src = await QuickRequests.get(f'{URL}?page={pageNum}', self._header)

        # Sending HTML to BS to parse:
        soup = BeautifulSoup(src, 'lxml')

        tag = soup.find_all("img")[camPosNum]
        image_url = tag.get("src")
        try:
            id = int(tag.get("id").replace("image", ''))  # Fetching InsecCam ID and converting to INT.
        except ValueError:
            print(f'{URL}?page={pageNum} and {camPosNum}')
            return
        # Creating a Camera object associated with the given ID, and returning it.

        cam = await Camera().create(id, image_url, self._header)
        return cam

    @property
    async def allowed_manufacturer(self):
        """A method for retrieving the set of manufactuerers

        :return: set(str)
        """
        return self._allowed_manufacturers

    @property
    async def allowed_countries(self):
        """A method for retrieving the set of countries

        :return: set(str)
        """
        return self._allowed_countries

    @property
    async def allowed_places(self):
        """A method for retrieving the set of places (parks, beaches, etc.)

        :return: set(str)
        """
        return self._allowed_places

    @property
    async def fetch_by_new(self):
        """Fetches a random camera from the new camera section.

        :return: Camera()
        """
        return await self.fetch_cam_from_url("http://www.insecam.org/en/bynew/")
    @property
    async def fetch_by_most_popular(self):
        """Fetches a random camera by most popular

        :return: Camera()
        """
        return await self.fetch_cam_from_url("http://www.insecam.org/en/byrating/")

    async def fetch_by_manufacturer(self, manufacturer: str):
        """Fetches a random camera by manufactuerer

        :return: Camera()
        """
        if await self.__check_manufacturers(manufacturer):
            return await self.fetch_cam_from_url(f"http://www.insecam.org/en/bytype/{manufacturer}/")
        else:
            raise InvalidManufacturer("[ICC] Your manufactuerer is not one supported by Inseccam.org")

    async def fetch_by_country(self, country_code):
        """Fetches a random camera by country code

        :return: Camera()
        """
        if await self.__check_country_code(country_code):
            return await self.fetch_cam_from_url(f"http://www.insecam.org/en/bycountry/{country_code}/")

    async def fetch_by_places(self, place):
        """Fetches a random camera by place

        :return: Camera()
        """
        if await self.__check_places(place):
            return await self.fetch_cam_from_url(f"http://www.insecam.org/en/bytag/{place}/")

    async def __check_places(self, place: str):
        """Function to check if a place is in the set of places.

        :return: bool
        """
        result = False

        if place in await self.allowed_places:
            result = True

        return result

    async def __check_country_code(self, country_code):
        """Function to check if a country code is in the set of country codes

        :return: bool
        """
        result = False

        if country_code in await self.allowed_countries:
            result = True

        return result

    async def __check_manufacturers(self, name: str):
        """Function to check if a manufactuerer is in the set of manufactuerers

        :return: bool
        """
        status = False

        if name in self._allowed_manufacturers:
            status = True

        return status


    async def __fetch_country_dict(self, header=None):
        countries = set()

        src = await QuickRequests.get("http://www.insecam.org/en/jsoncountries/", header=header, json=True)
        src = src['countries']

        return src

    async def __fetch_places_dict(self, header=None):
        src = await QuickRequests.get("http://www.insecam.org/en/jsontags/", header=header, json=True)
        src = src['tags']

        return src

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

    async def __fetch_page_num(self, URL):
        pageNum = 1

        src = await QuickRequests.get(URL, self._header)
        # Sending HTML to BS to parse:
        soup = BeautifulSoup(src, 'lxml')
        # Parsing out the max page number, and cleaning up parsed result:

        try:
            raw_maxPageNum = str(soup.find("ul", {"class": "pagination"}).find("script"))
            maxPageNum = int(raw_maxPageNum[43:-20])
            # Generating random page from the max page number.
            pageNum = randrange(1,maxPageNum)
        except AttributeError:
            pass

        return pageNum