import InsecamPy
import asyncio


async def main():
    # creates a crawler instance.
    crawler = await InsecamPy.crawler()

    # fetches a random russian camera
    cam = await crawler.fetch_by_country("RU")

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
    Insecam URL: http://www.insecam.org/en/view/949848/ 
    Camera Manufacturer: Hi3516 
    City: Krasnodar 
    Country: Russian Federation 
    Country Code: RU 
    Cam Description: None 
    Cam direct view link: http://77.39.112.156:80/webcapture.jpg?command=snap&channel=1?COUNTER 
    Insecam ID: 949848 
    GPS CORDS: ('5.04880', '8.97250') 
    Region: Krasnodarskiy Kray 
    Zipcode: 350000 
    Format: image/jpeg 
    Is JPEG format: True 
    
    """


if __name__ == '__main__':
    asyncio.run(main())

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
