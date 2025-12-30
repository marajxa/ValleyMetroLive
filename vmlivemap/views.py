from django.views.generic import TemplateView
import folium
import logging

import vmlivemap
from vmlivemap.accessors.vmlivemap import phxopendataaccessor, weatherapiaccessor
from vmlivemap.exceptions import InternalServerError
from vmlivemap.models import Stop
from vmlivemap.utils import drawingutil


def get_points():
    points = []
    try:
        response = phxopendataaccessor.get_valley_metro_gtfs_rt_data()
        for data_point in response.json()['entity']:
            if 'trip' in data_point['vehicle']:
                trip = data_point['vehicle']['trip']['routeId']
                if trip in ['A','B','S']:
                    vehicle_type = 'light_rail'
                else:
                    vehicle_type = 'bus'
                terminus = data_point['vehicle']['vehicle']['label'] if 'vehicle' in data_point['vehicle'] and 'label' in data_point['vehicle']['vehicle'] else ""
                speed = round(data_point['vehicle']['position']['speed']) if 'speed' in data_point['vehicle']['position'] else 0
                points.append({'location': [data_point['vehicle']['position']['latitude'], data_point['vehicle']['position']['longitude']],
                               'bearing': round(data_point['vehicle']['position']['bearing']), 'route': trip, 'terminus': terminus,
                               'vehicle_type': vehicle_type, 'speed': speed})
    except InternalServerError as e:
        logging.log(level=logging.ERROR, msg=e.message)
    finally:
        return points

def get_stops():
    stops = []
    for stop in Stop.objects.all():
        weather_f = ''
        try:
            response = weatherapiaccessor.get_weather_data_by_location(stop.latitude, stop.longitude)
            weather_f = str(response.json()['current']['temp_f'])
        except InternalServerError as e:
            logging.log(level=logging.ERROR, msg=e.message)
        stops.append({'stop_id': stop.stop_number, 'name': stop.stop_name, 'weather_f': weather_f, 'location':[stop.latitude, stop.longitude]})
    return stops


class MapView(TemplateView):
    template_name = 'vmlivemap/map.html'

    def get_context_data(self, **kwargs):
        figure = folium.Figure()

        vm_map = folium.Map(
            location=[33.448, -112.073],
            zoom_start=11,
            tiles='OpenStreetMap')

        vm_map.add_to(figure)

        for point in get_points():
            drawingutil.draw_vehicle_marker(point).add_to(vm_map)

        for stop in get_stops():
            drawingutil.draw_bus_stop(stop).add_to(vm_map)

        figure.render()
        return {"map": figure}
