from flask import request

from .exceptions import InvalidAccessKeyId

def basic(username, password):
    """ Returns a basic_auth-like AWS Signature v2 authentication function.
    """
    def authenticate(access, secret):
        if access != username:
            raise InvalidAccessKeyId(access)

        # TODO perform digest and compare signatures

        return {
            'username': access,
        }
