class AuthenticationError(Exception):
    """Authentication Error
    """

class InvalidAccessKeyId(AuthenticationError):
    """Invalid Access Key ID Error
    """

class SignatureDoesNotMatch(AuthenticationError):
    """Signature Does Not Match Error
    """
