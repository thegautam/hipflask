import nltk

from flask import request
from flask_restful import Resource

from .location import Location


class WeatherIntent():
    def _get_weather(self, name, lat, lng):
        return '{} is 51F and raining.'.format(name)

    def process(self, message):
        loc = Location(message)
        if not loc.parsed:
            return False, 'I couldn\'t identify the location for weather.'
        weather = self._get_weather(loc.locality_short, loc.lat, loc.lng)
        return weather


class UnknownIntent():
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
            name = data['name']
            return self._text_response('Hello, {}!'.format(name))
        else:
            message = data['text']
            intent = self._get_intent(message)
            response = intent.process(message)
            return self._text_response(response)
