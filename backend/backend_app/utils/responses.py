from flask import jsonify
from http import HTTPStatus


def success_response(
    *,
    message: str = "Success",
    data: dict | None = None,
    status: HTTPStatus = HTTPStatus.OK,
):

    response = {"success": True, "message": message, "data": data}

    return jsonify(response), status


def error_response(
    *,
    message: str = "Error",
    errors: str | None = None,
    status: HTTPStatus = HTTPStatus.BAD_REQUEST,
):

    response = {"success": False, "message": message, "errors": errors}

    return jsonify(response), status
