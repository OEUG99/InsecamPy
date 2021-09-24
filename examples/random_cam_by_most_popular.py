import InsecamPy
import asyncio


async def main():
    # creates a crawler instance.
    crawler = await InsecamPy.crawler()

    # fetches a random camera from the msot popular catagory.
    cam = await crawler.fetch_by_most_popular

    print("Our Park Camera: \n"
          f"Insecam URL: {await cam.url} \n"
          f"Camera Manufacturer: {await cam.manufacturer} \n"
          f"City: {await cam.city} \n"
          f"Country: {await cam.country} \n"
          f"Country Code: {await cam.country_code} \n"
          f"Cam Description: {await cam.description} \n"  # not all cameras have descriptions.
          f"Cam direct view link: {await cam.direct_url} \n"
          f"Insecam ID: {await cam.id} \n"
          f"GPS CORDS: {await cam.latitude, await cam.longitude} \n"
          f"Region: {await cam.region} \n"
          f"Zipcode: {await cam.zip} \n"
          f"Format: {await cam.format} \n"
          f"Is JPEG format: {await cam.jpeg_cam_check()} \n")

    """ Example Output:
    
    Our Park Camera: 
    Insecam URL: http://www.insecam.org/en/view/876238/ 
    Camera Manufacturer: Mobotix 
    City: Wroclaw 
    Country: Poland 
    Country Code: PL 
    Cam Description: None 
    Cam direct view link: http://178.183.157.187:8084/cgi-bin/faststream.jpg?stream=half&fps=15&rand=COUNTER 
    Insecam ID: 876238 
    GPS CORDS: ('1.10000', '7.03333') 
    Region: Dolnoslaskie 
    Zipcode: 54-622 
    Format: multipart/x-mixed-replace; boundary="MOBOTIX_Fast_Serverpush" 
    Is JPEG format: False 
    
    
    """


if __name__ == '__main__':
    asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
