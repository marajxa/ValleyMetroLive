import os
import requests
from vmlivemap.exceptions import InternalServerError

def get_valley_metro_gtfs_rt_vehicle_location_data():
    vm_api_key = os.environ.get('VALLEY_METRO_API_KEY')
    url = f"https://mna.mecatran.com/utw/ws/gtfsfeed/vehicles/valleymetro?apiKey={vm_api_key}&asJson=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        raise InternalServerError("Error accessing the GTFS-RT vehicle location data from Valley Metro.")

def get_valley_metro_gtfs_rt_service_alert_data():
    vm_api_key = os.environ.get('VALLEY_METRO_API_KEY')
    url = f"https://mna.mecatran.com/utw/ws/gtfsfeed/alerts/valleymetro?apiKey={vm_api_key}&asJson=true"
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        raise InternalServerError("Error accessing the GTFS-RT service alert data from Valley Metro.")
