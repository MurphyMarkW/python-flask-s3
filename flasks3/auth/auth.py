import re
from functools import wraps

from flask import current_app
from flask import request

from .exceptions import AuthenticationError


AWS_AUTH_REGEX = '^AWS (?P<access>[^:]+):(?P<secret>[^:]+)$'
aws_auth_regex = re.compile(AWS_AUTH_REGEX)


def authenticate(f):
    """Authenticates request and injects user information.
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('authorization', None)

        if auth is None:
            return f(*args, user={}, **kwargs)

        match = aws_auth_regex.match(auth)
        if not match:
            raise AuthenticationError('malformed authorization string')

        access = match.group('access')
        secret = match.group('secret')

        user = current_app.config['flasks3']['authenticate'](access, secret)

        return f(*args, user=user, **kwargs)

    return decorated
