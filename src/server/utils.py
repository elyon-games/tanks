from flask import jsonify
from common.errors import generateError

def formatRes(code, data):
    return jsonify({
        "error": False,
        "message": "GOOD",
        "data": data,
        "code": code
    }), 200

def formatErrorRes(code, message):
    return jsonify(generateError(code, message)), 500