# This module comes equipt with a slew of AWS HMAC digest algorithms
# for use in conjunction with the registered authentication callback.
# This is intended to make the blueprint more 'batteries included'
# without requiring use of said batteries. For instance, if the user
# wishes to have a separate system perform the auth and not store any
# sensitive information, such as secret keys, in memory.

def generate_signature(access, secret, version='4'):
    """Generate the AWS Signature for the given request context.
    """
    # TODO FIXME IMPLEMENT ME
    return generate_signature_v4(access, secret)

def generature_signature_v4(access, secret):
    """Generate the AWS Signature v4 for the given request context.
    """
    # TODO FIXME IMPLEMENT ME
    return '123'
