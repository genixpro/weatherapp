from pyramid.config import Configurator

from pyramid.renderers import JSON
import logging

def group_for_user(userid, request):
    """ All logged in users are considered accounts."""
    return ["group:account"]

class WeatherApplication:
    def __init__(self, global_config, **settings):
        # Create the pyramid configurator
        config = Configurator(settings=settings)
        
        # Add this application object to the registry
        config.registry.application = self
        def add_application(request):
            return self
        config.add_request_method(add_application, 'application', reify=True)
        
        # Setup JSON serialization to include indentation (e.g. pretty printed)
        config.add_renderer('formatted_json', JSON(indent=4))
        
        # Setup the static views and routes
        config.add_static_view('css', 'static/css', cache_max_age=3600)
        config.add_static_view('img', 'static/img', cache_max_age=3600)
        config.add_static_view('font', 'static/font', cache_max_age=3600)
        config.add_static_view('js', 'static/js', cache_max_age=3600)
        config.add_route('weather', '/cityweathers')
        config.add_route('index', '')
        config.scan()
        
        
        self.app = config.make_wsgi_app()

    def __call__(self, environ, start_response):
        """This processes an incoming request from WSGI. """
        return self.app(environ, start_response)



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    return WeatherApplication(global_config, **settings)


