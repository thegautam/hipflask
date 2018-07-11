from flask import Flask, request
from flask_restful import Api, Resource
from flask_cors import CORS
from .messages import Message

def setup_app():
    # Setup the app
    app = Flask(__name__)
    CORS(app)
    api = Api(app)

    # Setup the routes
    api.add_resource(Message, '/chat/messages')
    return app, api

app, api = setup_app()

if __name__ == '__main__':
    app.run(debug=True, port=9000)