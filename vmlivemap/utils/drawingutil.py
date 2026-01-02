import folium
import os
from PIL import Image

IMG_DIR = os.getcwd() + '/vmlivemap/static/vmlivemap/image/'

def draw_vehicle_marker(point):
    file_path = f"{IMG_DIR}generated_image/{point['vehicle_type']}_{str(point['bearing'])}.png"
    if not os.path.exists(file_path):
        image = Image.open(f"{IMG_DIR}{point['vehicle_type']}.png")
        if 0 < point['bearing'] < 180:
            image = image.transpose(Image.Transpose.FLIP_LEFT_RIGHT).rotate(90 - point['bearing'])
        else:
            image = image.rotate(270 - point['bearing'])
        image.save(file_path, "PNG")
    icon = folium.CustomIcon(icon_image=file_path, icon_size=(50,35), icon_anchor=(25,17))
    speed_text = ""
    if point['vehicle_type'] == 'bus':
        speed_text = f"<p>Speed: {str(round(point['speed']))}mph</p>"
    alert_text = ""
    if 'alerts' in point:
        alert_text = generate_alert_text(point['alerts'])
    popup_text = f"""
    <div style="width: 150px">
    <h3>Route {point['route']} to {point['terminus']}</h3>
    {alert_text}
    {speed_text}
    </div>
    """
    return folium.Marker(location=point['location'], icon=icon, popup=popup_text)

def draw_bus_stop(stop):
    icon = folium.Icon(color='green', icon_color='purple', prefix='fa', icon='hand')
    alert_text = ""
    if 'alerts' in stop:
        alert_text = generate_alert_text(stop['alerts'])
    popup_text = f"""
    <div style="width: 150px">
    <h3>Stop {stop['stop_id']}</h3>
    <h4>{stop['name']}</h4>
    {alert_text}
    <p>Current temperature: {stop['weather_f']}F</p>
    </div>
    """
    return folium.Marker(location=stop['location'], icon=icon, popup=popup_text)

def generate_alert_text(alerts):
    alert_text = """<p style="color: red;font-weight:bold">Service Alerts!</p>"""
    for alert in alerts:
        alert_text = alert_text + f"""
            <details>
                <summary style="color: blue">{alert['title']}</summary>
                <p>{alert['body']}</p>
            </details>
            """
    return alert_text