

WeatherApplication.Cityweather = DS.Model.extend({
  name: DS.attr('string'),
  api_temperature: DS.attr('string'),
  scrape_temperature: DS.attr('string'),
  latitude: DS.attr('number'),
  longitude: DS.attr('number'),
});


