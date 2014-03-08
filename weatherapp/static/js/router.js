
WeatherApplication.Router.reopen({
  location: 'hash'
});

WeatherApplication.Router.map(function()
{

});



WeatherApplication.IndexRoute = Ember.Route.extend({
    model: function()
    {
        weather = this.store.find("Cityweather");
        return weather;
    },
    renderTemplate: function()
    {
        this.render('index');
        var self = this;
        function setup_weather_table()
        {
            $('#weather').dataTable({
                "sPaginationType": "full_numbers"
            });
            
            var mapOptions = {
              center: new google.maps.LatLng(57.04073,-100.561525),
              zoom: 2
            };
            
            var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
            
            // For each of the first 10 cities in the list of cities, we create a marker on the map
            var onSuccess = function(weathers) {
                weathers.forEach(function(weather, index, enumerable)
                {
                    if(index < 10)
                    {
                        var title = weather.get("name") + ": " + weather.get("api_temperature") + " c";
                        var markeroptions = {
                            position: new google.maps.LatLng(weather.get("latitude"), weather.get("longitude")),
                            map: map,
                            title: title,
                        };
                    
                        var contentString = '<h3 id="firstHeading" class="firstHeading">' + title + '</h3>';

                        var infowindow = new google.maps.InfoWindow({
                            content: contentString
                        });

                        var marker = new google.maps.Marker(markeroptions);

                        google.maps.event.addListener(marker, 'click', function() {
                            infowindow.open(map, marker);
                        });
                        
                        marker.setMap(map);
                    }
                });
            };

            var onFail = function(post) {
              // deal with the failure here
            };
            
            this.model().then(onSuccess, onFail);
            
            if(window.countdown_interval != undefined)
            {
                window.clearInterval(window.countdown_interval);
            }

            window.countdown = 30;
            // Schedule the automatic reloading of the page
            window.countdown_interval = window.setInterval(function(){
                window.countdown -= 1;
                if(window.countdown <= 0)
                {
                    self.refresh();
                    window.countdown = 30;
                }
                else
                {
                    $('#countdown').html(window.countdown + " seconds until refresh");
                }                
            }, 1000);
        }
        
        Ember.run.scheduleOnce('afterRender', this, setup_weather_table);
    },
    actions: {
        reload: function()
        {
            this.refresh();
        },
    },
});
