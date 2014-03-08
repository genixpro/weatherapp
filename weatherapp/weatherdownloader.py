import requests
import threading
import time
import datetime
from HTMLParser import HTMLParser
from pprint import pprint
import string

class WeatherDownloadThread(threading.Thread):
    """ This class represents a thread which polls both the Openweathermap server and Theweathernetwork to download weather data on canadian cities and storing
        it in a cache, updating roughly every five minutes. """
    # This is the list of cities in Canada to poll. The values are part of the path segment on http://www.theweathernetwork.com/
    cities = {  'Toronto' : "http://weather.canoe.ca/Weather/CityTorontoON.html",
                'Montreal' : "http://weather.canoe.ca/Weather/CityMontrealQC.html",
                'Calgary' : "http://weather.canoe.ca/Weather/CityCalgaryAB.html",
                'Ottawa' : "http://weather.canoe.ca/Weather/CityOttawaON.html",
                'Edmonton' : "http://weather.canoe.ca/Weather/CityEdmontonAB.html",
                'Mississauga' : "http://weather.canoe.ca/Weather/CityMississaugaON.html",
                'Winnipeg' : "http://weather.canoe.ca/Weather/CityWinnipegMB.html",
                'Vancouver' : "http://weather.canoe.ca/Weather/CityVancouverBC.html",
                'Brampton' : "http://weather.canoe.ca/Weather/CityBramptonON.html",
                'Hamilton' : "http://weather.canoe.ca/Weather/CityHamiltonON.html",
                'Quebec City' : "http://weather.canoe.ca/Weather/CityQuebecQC.html",
                'Surrey' : "http://weather.canoe.ca/Weather/CitySurreyBC.html",
                'Laval' : "http://weather.canoe.ca/Weather/CityLavalQC.html",
                'Halifax' : "http://weather.canoe.ca/Weather/CityHalifaxNS.html",
                'London' : "http://weather.canoe.ca/Weather/CityLondonON.html",
                'Markham' : "http://weather.canoe.ca/Weather/CityMarkhamON.html",
                'Vaughan' : "http://weather.canoe.ca/Weather/CityVaughanON.html",
                'Gatineau' : "http://weather.canoe.ca/Weather/CityGatineauQC.html",
                'Longueuil' : "http://weather.canoe.ca/Weather/CityLongueuilQC.html",
                'Burnaby' : "http://weather.canoe.ca/Weather/CityBurnabyBC.html",
                'Saskatoon' : "http://weather.canoe.ca/Weather/CitySaskatoonSK.html",
                'Kitchener' : "http://weather.canoe.ca/Weather/CityKitchenerON.html",
                'Windsor' : "http://weather.canoe.ca/Weather/CityWindsorON.html",
                'Regina' : "http://weather.canoe.ca/Weather/CityReginaSK.html",
                'Oakville' : "http://weather.canoe.ca/Weather/CityOakvilleON.html",
                'Burlington' : "http://weather.canoe.ca/Weather/CityBurlingtonON.html",
                'Fredericton' : "http://weather.canoe.ca/Weather/CityFrederictonNB.html",
                'Charlottetown' : "http://weather.canoe.ca/Weather/CityCharlottetownPE.html",
                'St. Johns' : "http://weather.canoe.ca/Weather/CitySt.JohnsNL.html",
                }
    
    daemon = True
    
    def __init__(self):
        super(WeatherDownloadThread, self).__init__()
        self.api_temps = {}
        self.scrape_temps = {}
        self.coordinates = {}
        
        for city in self.cities:
            self.api_temps[city] = 0 # Default to 0
            self.scrape_temps[city] = 0 # Default to 0
            self.coordinates[city] = [0,0] # Default to [0,0]
        
        self.cont = True
    
    def run(self):
        """This is meant to be run on its own thread. It will continuously download weather data for important canadian cities"""
        target = datetime.datetime.now()
        
        while self.cont:
            # Increase the target time by 5 minutes.
            target = target + datetime.timedelta(seconds = 60 * 5)
            
            # Download current temperature
            self.download_current_temps()
            
            # Calculate the time remaining until the target time. This keeps us on pace to do one loop exactly every 5 minutes
            time_to_sleep = target - datetime.datetime.now()
            
            # Only sleep if the number is positive. If the number is negative, this means that the downloading is taking
            # longer then five minutes to complete. In that case we move immedietly onto the next loop
            if time_to_sleep.total_seconds() > 0:
                # Sleep in the total amount in 100ms intervals. This makes it so that if
                # self.cont is changed to False, the loop will end instantly rather then
                # taking a long time to exit.
                for n in xrange(int(time_to_sleep.total_seconds()*10)):
                    time.sleep(0.1)

    def download_api_temps(self):
        """ This method will download all of the current temperatures from api.openweathermap.org and store them in the city_temps dictionary."""
        for city in self.cities.keys():
            # Keep retrying until successful
            success = False
            while not success:
                try:
                    print "Downloading from API for city " + city
                    response = requests.get("http://api.openweathermap.org/data/2.5/forecast?q=%s,ca&mode=json" % city).json()
                    self.coordinates[city] = [response['city']['coord']['lat'], response['city']['coord']['lon']]
                    
                    current_temp = float(response['list'][0]['main']['temp']) - 273.15
                    self.api_temps[city] = current_temp
                    success = True
                except ValueError as e:
                    print "City not found: " + city
                    success = True # Ignore if the city isn't found
                except Exception as e:
                    print e
    
    def download_scrape_temps(self):
        for city,citypath in self.cities.iteritems():
            # Keep retrying until successful
            success = False
            while not success:
                try:
                    print "Downloading from Canoe Weather for city " + city
                    response = requests.get(citypath)
                    
                    # Create a parser to scrape the request for the temperature
                    class WeatherScraper(HTMLParser):
                        def __init__(self):
                            HTMLParser.__init__(self)
                            self.next_data_is_temp = False
                            self.current_temp = None
                        def handle_starttag(self, tag, attrs):
                            attrsd = dict(attrs)
                            if tag == 'p':
                                if 'class' in attrsd and attrsd[u'class'] == u'temperature':
                                    self.next_data_is_temp = True
                        def handle_endtag(self, tag):
                            pass
                        def handle_data(self, data):
                            if self.next_data_is_temp:
                                if self.current_temp is None:
                                    self.current_temp = data
                        
                    scraper = WeatherScraper()
                    scraper.feed(response.text)
                            
                    self.scrape_temps[city] = float(filter(lambda x: x.isdigit() or x == '-' or x == '.', scraper.current_temp))
                    success = True
                except ValueError as e:
                    print e
                    print "City not found: " + city
                    success = True # Ignore if the city isn't found
                #except Exception as e:
                #    print e
    
    def download_current_temps(self):
        """ This method will download all of the current temperatures from bothe places."""
        self.download_scrape_temps()
        self.download_api_temps()

            
 
    @classmethod
    def launch_download_weather_thread(cls):
        download_thread = WeatherDownloadThread()
        download_thread.start()
        return download_thread
    
    def shutdown(self):
        download_thread.cont = False
        download_thread.join()
    
    
download_thread = WeatherDownloadThread.launch_download_weather_thread()

def get_all_weather():
    weather = [{'name' : city,
              'api_temperature' :  "%0.2f" % download_thread.api_temps[city],
              'latitude' :  download_thread.coordinates[city][0],
              'longitude' :  download_thread.coordinates[city][1],
              'scrape_temperature' :  "%0.2f" % download_thread.scrape_temps[city]} for city in download_thread.cities.keys()]
     
    # Sort the weather by temperature
    def weathercmp(lhs, rhs):
        return cmp(float(lhs['api_temperature']), float(rhs['api_temperature']))
    
    weather = sorted(weather, weathercmp)
    
    for number, d in enumerate(weather):
        d['id'] = "%03d" % (number + 1)
    
    return weather

