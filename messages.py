''' Main module to handle messages '''

from flask import request
from flask_restful import Resource
import forecastio

from .location import Location

DARKSKY_KEY = '8b4d5ca925446f9db4f7d7d0aac8b40c'


class JoinIntent():
    ''' Simple handler for new user '''
    def process(self, name):
        return 'Hello, {}!'.format(name)


class WeatherIntent():
    ''' Handler for weather intent '''
    def _get_weather(self, name, lat, lng):
        forecast = forecastio.load_forecast(DARKSKY_KEY, lat, lng).currently()
        return '{} is {}F and {}.'.format(name, round(forecast.temperature),
                                          forecast.summary.lower())

    def process(self, message):
        loc = Location(message)
        if not loc.parsed:
            return False, 'I couldn\'t identify the location for weather.'
        weather = self._get_weather(loc.locality_short, loc.lat, loc.lng)
        return weather


class UnknownIntent():
    ''' Generic handler '''
    def process(self, message):
        return "Sorry, I don't understand that."


class Message(Resource):

    def _error_response(self, message):
        return {"error": message}, 400

    def _text_response(self, message):
        return {"messages": [{"type": "text", "text": message}]}, 200

    def _get_intent(self, message):
        ''' Get the intent class from the message '''
        if 'weather' in message.lower().split():
            return WeatherIntent()

        return UnknownIntent()

    def post(self):
        data = request.form

        # Validate payload is correct
        action = data.get('action')
        if not action or action not in ['join', 'message']:
            return self._error_response('Invalid action')

        if action == 'join':
            message = data['name']
            intent = JoinIntent()
        else:
            message = data['text']
            intent = self._get_intent(message)

        response = intent.process(message)
        return self._text_response(response)
