from django.views.generic import TemplateView
import folium
import logging
import time

from vmlivemap.accessors.vmlivemap import phxopendataaccessor, weatherapiaccessor
from vmlivemap.exceptions import InternalServerError
from vmlivemap.models import Stop
from vmlivemap.utils import drawingutil


class MapView(TemplateView):
    template_name = 'vmlivemap/map.html'

    def get_context_data(self, **kwargs):
        figure = folium.Figure()

        vm_map = folium.Map(
            location=[33.448, -112.073],
            zoom_start=11,
            tiles='OpenStreetMap')

        vm_map.add_to(figure)

        route_alerts, stop_alerts = process_alerts()

        for point in get_points():
            if point['route'] in route_alerts:
                point['alerts'] = route_alerts[point['route']]
            drawingutil.draw_vehicle_marker(point).add_to(vm_map)

        for stop in get_stops():
            if stop['stop_id'] in stop_alerts:
                stop['alerts'] = stop_alerts[stop['stop_id']]
            drawingutil.draw_bus_stop(stop).add_to(vm_map)

        figure.render()
        return {"map": figure}

def get_points():
    points = []
    try:
        response = phxopendataaccessor.get_valley_metro_gtfs_rt_vehicle_location_data()
        for data_point in response.json()['entity']:
            if 'trip' in data_point['vehicle']:
                route = data_point['vehicle']['trip']['routeId']
                if route in ['A', 'B', 'S']:
                    vehicle_type = 'light_rail'
                else:
                    vehicle_type = 'bus'
                terminus = data_point['vehicle']['vehicle']['label'] if 'vehicle' in data_point['vehicle'] and 'label' in data_point['vehicle']['vehicle'] else ""
                speed = round(data_point['vehicle']['position']['speed']) if 'speed' in data_point['vehicle']['position'] else 0
                points.append({'location': [data_point['vehicle']['position']['latitude'],
                                            data_point['vehicle']['position']['longitude']],
                                'bearing': round(data_point['vehicle']['position']['bearing']), 'route': route,
                                'terminus': terminus,
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
        stops.append({'stop_id': stop.stop_number, 'name': stop.stop_name, 'weather_f': weather_f,
                        'location': [stop.latitude, stop.longitude]})
    return stops

def process_alerts():
    route_alerts = {}
    stop_alerts = {}
    response = phxopendataaccessor.get_valley_metro_gtfs_rt_service_alert_data()
    for alert in response.json()['entity']:
        is_active = False
        for active_period in alert['alert']['activePeriod']:
            if int(active_period['start']) < int(time.time()) < int(active_period['end']):
                is_active = True
        if is_active:
            title = next(x['text'] for x in alert['alert']['headerText']['translation'] if x['language'] == 'en')
            body = next(
                x['text'] for x in alert['alert']['descriptionText']['translation'] if x['language'] == 'en')
            for entity in alert['alert']['informedEntity']:
                if 'routeId' in entity:
                    if entity['routeId'] not in route_alerts:
                        route_alerts[entity['routeId']] = [{'alert_id': alert['id'], 'title': title, 'body': body}]
                    elif not next((x for x in route_alerts[entity['routeId']] if 'title' in x and x['title'] == title), None):
                        route_alerts[entity['routeId']].append({'title': title, 'body': body})
                if 'stopId' in entity:
                    if entity['stopId'] not in stop_alerts:
                        stop_alerts[entity['stopId']] = [{'alert_id': alert['id'], 'title': title, 'body': body}]
                    elif not next((x for x in stop_alerts[entity['stopId']] if 'title' in x and x['title'] == title), None):
                        stop_alerts[entity['stopId']].append({'title': title, 'body': body})
    return route_alerts, stop_alerts
