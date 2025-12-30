import folium
import os
from PIL import Image

IMG_DIR = os.getcwd() + '/vmlivemap/static/vmlivemap/image/'

def draw_vehicle_marker(point):
    file_path = IMG_DIR + 'generated_image/' + point['vehicle_type'] + '_' + str(point['bearing']) + '.png'
    if not os.path.exists(file_path):
        image = Image.open(IMG_DIR + point['vehicle_type'] + '.png')
        if 0 < point['bearing'] < 180:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT).rotate(90 - point['bearing'])
        else:
            image = image.rotate(270 - point['bearing'])
        image.save(file_path, "PNG")
    icon = folium.CustomIcon(icon_image=file_path, icon_size=(50,35), icon_anchor=(25,17))
    popup_text = "Route " + point['route'] + " to " + point['terminus']
    if point['vehicle_type'] == 'bus':
        popup_text = popup_text + "\n" + "Speed: " + str(round(point['speed'])) + "mph"
    return folium.Marker(location=point['location'], icon=icon, popup=popup_text)

def draw_bus_stop(stop):
    icon = folium.Icon(color='green')
    popup_text = f"Stop {stop['stop_id']} \n {stop['name']} \n The current temperature is {stop['weather_f']}F"
    return folium.Marker(location=stop['location'], icon=icon, popup=popup_text)