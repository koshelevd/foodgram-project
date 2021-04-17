"""Exceptions of the 'users' app."""
from rest_framework.exceptions import APIException


class BadRequest(APIException):
    """Custom API exception to raise 400 status."""
    status_code = 400
    default_detail = 'Bad request.'


class ServerError(APIException):
    """Custom API exception to raise 500 status."""
    status_code = 500
    default_detail = 'Internal server error.'
