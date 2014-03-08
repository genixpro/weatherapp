

window.WeatherApplication = Ember.Application.create();

WeatherApplication.ApplicationController = Ember.Controller.extend({

});


WeatherApplication.Store = DS.Store.extend({
    revision: 1,
    adapter: 'DS.RESTAdapter'
});

