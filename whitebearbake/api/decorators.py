# Standard imports
import datetime
from functools import wraps


# Module imports
import uuid
from flask import abort, jsonify, make_response, request


def jSend(fn):
    """ jSend decorator """
    @wraps(fn)
    def decorated(*args, **kwargs):
        result = fn(*args, **kwargs)
        status_code = result.get('status_code', '500')
        result['status'] = result.get('status', 'error')
        result['message'] = result.get('message', 'Internal Server Error')
        result['data'] = result.get('data', None)
        result['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result['uuid'] = result.get('uuid', uuid.uuid4())
        response = make_response(jsonify(result), status_code)
        response.headers['Content-Type'] = 'application/json'
        return response
    return decorated