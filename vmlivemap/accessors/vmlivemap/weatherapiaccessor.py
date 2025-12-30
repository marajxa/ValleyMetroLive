import os
import requests
from vmlivemap.exceptions import InternalServerError

def get_weather_data_by_location(latitude, longitude):
    weather_api_key = os.environ.get('WEATHER_API_KEY')
    location = str(latitude) + "," + str(longitude)
    url = f"https://api.weatherapi.com/v1/current.json?q={location}&key={weather_api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        return response
    else:
        raise InternalServerError("Error accessing the live weather data from Weather API.")