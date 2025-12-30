import requests
from vmlivemap.exceptions import InternalServerError

def get_valley_metro_gtfs_rt_data():
    url = 'https://mna.mecatran.com/utw/ws/gtfsfeed/vehicles/valleymetro?apiKey=4f22263f69671d7f49726c3011333e527368211f&asJson=true'
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        raise InternalServerError("Error accessing the GTFS-RT data from Valley Metro.")
