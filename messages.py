from flask import request
from flask_restful import Resource

class Message(Resource):

    def _error_response(self, message):
        return { "error": message }, 400

    def _text_response(self, message):
        return { "messages":[{ "type": "text", "text": message }]}, 200

    def post(self):
        data = request.form

        # Validate payload is correct
        action = data.get('action')
        if not action or not action in ['join', 'message']:
            return self._error_response('Invalid action')

        if action == 'join':
            name = data['name']
            return self._text_response('Hello, {}!'.format(name))
        else:
            output = "message: " + data['text']
            return { "messages":[{ "type":"text", "text":output }]}, 200
