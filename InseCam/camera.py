import requests
from bs4 import BeautifulSoup
import functools
import asyncio
class Camera():

    def __init__(self):

        self._header = None
        self._id = None
        self._country_code = None
        self._latitude = None
        self._longitude = None
        self._zip = None
        self._country = None
        self._region = None
        self._city = None
        self._timezone = None
        self._manufacturer = None
        self._description = None


    @classmethod
    async def create(cls, id: int, image_url: str, header=None):
        """Factory function. Essentially called when we want to create an object of this class.
        Basically, an async __init__.

        :param id: InseCam ID
        :param header: Optional. custom header to use.
        :return: class `InseCam.camera.Camera`
        """
        self = cls()

        self._id = id
        self._header = header
        self._image_url = image_url

        metadata = await self.__fetch_metadata(id)

        # Automatically assign values to the attirbutes.
        for key in metadata:
            setattr(self, f"_{key}", metadata[key])

        return self


    async def __fetch_metadata(self, id_: int):
        """ Fetches the meta data associated to a camera.

        :param id: The Insecam.org ID for a camera.
        :return dict: returns dictionary of camera meta data.
        """

        URL = f"http://www.insecam.org/en/view/{id_}/"
        cam_data = {}

        # Fetching the HTML from the URL:
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(None, lambda: requests.get(URL, headers=self._header, timeout=5))
        src = await future
        src = src.content

        # Sending HTML to BS to parse for the camera details:
        soup = BeautifulSoup(src, 'lxml')
        raw_metadata = soup.find_all('div', class_='camera-details__cell')
        raw_cam_description = soup.find('div', style="border:double 4px #949494; -moz-border-radius: 0px; "
                                                         + "-webkit-border-radius: 0px; border-radius: 5; "
                                                         + "line-height: 1.5; text-align: justify; word-spacing: 3px;")


        # Cleaning up parsed data, and adding it to our dictionary
        del raw_metadata[::2]


        # Adding the text of each <div> html element to our dictionary.
        cam_data["country_code"] = raw_metadata[1].text
        cam_data["latitude"] = raw_metadata[4].text
        cam_data["longitude"] = raw_metadata[5].text
        cam_data["zip"] = raw_metadata[6].text

        # All of these have an <a> element inside the <div>, hince the discrpency.
        cam_data["country"] = raw_metadata[0].find('a').text
        cam_data["region"] = raw_metadata[2].find('a').text
        cam_data["city"] = raw_metadata[3].find('a').text[1:] # We chop off a letter due to their being a random space.
        cam_data["timezone"] = raw_metadata[7].find('a').text
        cam_data["manufacturer"] = raw_metadata[8].find('a').text

        # Not all cameras have a description, if they do then we will update the attribute.
        if raw_cam_description is not None:
            cam_data["description"] = raw_cam_description.text # Not every camera has a discription, so this can be type None

        return cam_data

    @property
    async def insec_url(self):
        """
        :return: returns a string containing the url for the camera on InseCam.org
        """
        return f"https://www.insecam.org/en/view/{self._id}/"

    @property
    async def image_url(self):
        """
        :return: returns a string containing the images URL.
        """
        return self._image_url

    @property
    async def country_code(self):
        """Fetches the country code
        :rtype: str
        :return: returns a string containing the country code.
        """
        return self._country_code

    @property
    async def latitude(self):
        """Fetches the latidude
        :rtype: str
        :return: returns a string containing the latitude
        """
        return self._latitude

    @property
    async def longitude(self):
        """Fetches the longitude
        :rtype: str
        :return: returns a string containing the longitude
        """
        return self._longitude

    @property
    async def zip(self):
        """Fetches the zip code
        :rtype: str
        :return: returns a string containing the zip
        """
        return self._zip

    @property
    async def country(self):
        """Fetches the country
        :rtype: str
        :return: returns a string containing the country
        """
        return self._country

    @property
    async def region(self):
        """Fetches the region
        :rtype: str
        :return: returns a string containing the region
        """
        return self._region

    @property
    async def city(self):
        """Fetches the city
        :rtype: str
        :return: returns a string containing the city
        """
        return self._city

    @property
    async def timezone(self):
        """Fetches the city
        :rtype: str
        :return: returns a string containing the timezone
        """
        return self._timezone

    @property
    async def manufacturer(self):
        """Fetches the manufacturer
        :rtype: str
        :return: returns a string containing the manufacturer
        """
        return self._manufacturer

    @property
    async def description(self):
        """Fetches the discription, if the camera has one listed.
        :rtype: str, or None
        :return: Returns a string containing the description, or None.
        """
        return self._description