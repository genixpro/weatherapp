from pyramid.view import view_config
import requests
import weatherdownloader
from pprint import pprint



@view_config(route_name='index', renderer='weatherapp:templates/weather.mako')
def index(request):
    return {}


@view_config(route_name='weather', renderer='formatted_json')
def weather(request):
    data = {'Cityweather': weatherdownloader.get_all_weather()}
    
    pprint(data)
    return data

