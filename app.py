from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
api = Api(app)

class Message(Resource):
    def post(self):
        data = request.form
        output = "message: " + data['text']
        return { "messages":[{ "type":"text", "text":output }]}, 201

api.add_resource(Message, '/chat/messages')

if __name__ == '__main__':
    app.run(debug=True)