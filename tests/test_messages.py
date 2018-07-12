import itertools
import json
import os
import re
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


def check_get_text(result):
    ''' Helper method to get text message after checking for success '''
    assert result.status_code == SUCCESS_CODE, 'Invalid status'
    data = json.loads(result.data)
    messages = data['messages']
    assert messages[0]['type'] == 'text', 'Invalid type'
    return messages[0]['text']


def test_user_join(app):
    ''' User join should result in greeting '''
    name = "John"
    payload = {
        "action": "join",
        "user_id": 123456,
        "name": name
    }
    result = app.test_client().post(API, data=payload)
    response = check_get_text(result)
    assert response == 'Hello, {}!'.format(name), 'Invalid greeting'

locations = [('SF', 'SF'), ('seAttle', 'Seattle'), ('San Francisco', 'SF'),
             ('15213', 'Pittsburgh')]
messages = ['Weather in {}', 'what is weather in {}', '{} weather']


@pytest.mark.parametrize('message,location', 
                         itertools.product(messages, locations))
def test_weather(app, message, location):
    text = message.format(location[0])
    payload = {
        "action": "message",
        "user_id": 123456,
        "text": text
    }
    result = app.test_client().post(API, data=payload)
    response = check_get_text(result)
    assert re.match('{} is 51F and raining'.format(location[1]), response), \
        '{}: {}'.format(text, response)
