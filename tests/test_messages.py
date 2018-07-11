import json
import os
import sys
import tempfile

import pytest
from flask import Flask, request

from hipflask.app import setup_app
from hipflask.messages import Message

SUCCESS_CODE = 200
API = '/chat/messages'


@pytest.fixture
def app():
    ''' Create app for use in all tests '''
    app, _ = setup_app()
    return app


def assert_text_message(result, message):
    ''' Helper method to test text message success response '''
    assert result.status_code == SUCCESS_CODE, 'Invalid status'
    data = json.loads(result.data)
    messages = data['messages']
    assert messages[0]['type'] == 'text', 'Invalid type'
    assert messages[0]['text'] == message, 'Invalid greeting'


def test_user_join(app):
    ''' User join should result in greeting '''
    name = "John"
    payload = {
        "action": "join",
        "user_id": 123456,
        "name": name
    }
    result = app.test_client().post(API, data=payload)
    assert_text_message(result, 'Hello, {}!'.format(name))


def test_weather(app):
    city = "Seattle"
    payload = {
        "action": "message",
        "user_id": 123456,
        "text": "Weather in {}".format(city)
    }
    result = app.test_client().post(API, data=payload)
    assert_text_message(result, 'Hello, {}!'.format(city))

