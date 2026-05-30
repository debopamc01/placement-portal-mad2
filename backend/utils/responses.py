from flask import jsonify
from http import HTTPStatus


def success_response(
    *,
    message="Success",
    data=None,
    status=HTTPStatus.OK
):

    response = {
        "success": True,
        "message": message,
        "data": data
    }

    return jsonify(response), status


def error_response(
    *,
    message="Error",
    errors=None,
    status=HTTPStatus.BAD_REQUEST
):

    response = {
        "success": False,
        "message": message,
        "errors": errors
    }

    return jsonify(response), status