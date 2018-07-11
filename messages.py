from flask import request
from flask_restful import Resource


class WeatherIntent():
    def _get_location(self, message):
        words = message.split()
        for prev, curr in zip(words, words[1:]):
            print(prev)
            if prev == 'in':
                return curr

        return None

    def _get_weather(self, location):
        return '{} is 51F and raining.'.format(location)

    def process(self, message):
        location = self._get_location(message)
        weather = self._get_weather(location)
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
        if 'weather' in message.split():
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
            message = data['text'].lower()
            intent = self._get_intent(message)
            response = intent.process(message)
            return self._text_response(response)
