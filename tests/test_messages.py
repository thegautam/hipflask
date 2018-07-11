import json
import os
import sys
import tempfile

import pytest
from flask import Flask, request

from hipflask.app import setup_app
from hipflask.messages import Message

SUCCESS_CODE = 200

def test_user_join():
    app, _ = setup_app()
    url = '/chat/messages'
    name = "John"
    payload = {
        "action": "join",
        "user_id": 123456,
        "name": name
    }
    result = app.test_client().post(url, data=payload)
    assert result.status_code == SUCCESS_CODE, 'Invalid status'
    data = json.loads(result.data)
    messages = data['messages']
    assert messages[0]['type'] == 'text', 'Invalid type'
    assert messages[0]['text'] == 'Hello, {}!'.format(name), 'Invalid greeting'
