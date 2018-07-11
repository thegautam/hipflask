from flask import request
from flask_restful import Resource

class Message(Resource):
    def post(self):
        data = request.form
        output = "message: " + data['text']
        return { "messages":[{ "type":"text", "text":output }]}, 201
