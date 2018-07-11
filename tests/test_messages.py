import sys
import os
import tempfile
import pytest

from flask import Flask, request

from hipflask.messages import Message
from hipflask.app import setup_app

SUCCESS_CODE = 201

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
    assert result.data.messages[0].type == 'text', 'Invalid type'
    assert result.data.messages[0].text == 'Hello, {}!'.format(name), 'Invalid greeting'
