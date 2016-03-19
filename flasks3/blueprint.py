import sys

from xml.etree import ElementTree as et

import flask

from flask import request
from flask import Response

from .auth import authenticate

from .exceptions import AuthenticationError
from .exceptions import InvalidAccessKeyId
from .exceptions import SignatureDoesNotMatch
from .exceptions import NoSuchBucketError
from .exceptions import NoSuchKeyError

blueprint = flask.Blueprint('s3', __name__)
blueprint.config = dict()


@blueprint.route('/', methods=['GET'])
@authenticate
def get_service(user):
    """Return a list of buckets.
    """
    root = et.Element('ListAllMyBucketsResult')
    root.attrib['xmlns'] = 'http://s3.amazonaws.com/doc/2006-03-01'

    owner = et.SubElement(root, 'Owner')

    owner_id = et.SubElement(owner, 'ID')
    owner_id.text = '123'

    owner_name = et.SubElement(owner, 'DisplayName')
    owner_name.text = '123'

    buckets = et.SubElement(root, 'Buckets')

    for b in blueprint.driver.buckets(user):
        bucket = et.SubElement(buckets, 'Bucket')

        bucket_name = et.SubElement(bucket, 'Name')
        bucket_name.text = b

        bucket_date = et.SubElement(bucket, 'CreationDate')
        bucket_date.text = 'some_date'

    res = et.tostring(root)
    res = '<?xml version="1.0" encoding="UTF-8"?>'+res

    return res, 200

@blueprint.route('/<bucket>/', methods=['GET'])
@authenticate
def get_bucket(bucket, user):
    """Returns a list of keys within a bucket.
    """
    root = et.Element('ListBucketResult')
    root.attrib['xmlns'] = 'http://s3.amazonaws.com/doc/2006-03-01'

    name = et.SubElement(root, 'Name')
    name.text = bucket

    prefix = et.SubElement(root, 'Prefix')

    marker = et.SubElement(root, 'Marker')

    max_keys = et.SubElement(root, 'MaxKeys')
    max_keys.text = '1000'

    is_truncated = et.SubElement(root, 'IsTruncated')
    is_truncated.text = 'false'

    for i, k in enumerate(blueprint.driver.keys(bucket, user)):

        # Limit number of keys returned.
        if i >= 1000:
            is_truncated.text = 'true'
            marker.text = k
            break

        content = et.SubElement(root, 'Contents')

        key = et.SubElement(content, 'Key')
        key.text = k

        mod = et.SubElement(content, 'LastModified')
        mod.text = '2009-10-12T17:50:30.000Z'

        tag = et.SubElement(content, 'ETag')
        tag.text = 'fba9dede5f27731c9771645a39863328'

        size = et.SubElement(content, 'Size')
        size.text = '1234567890'

        storage = et.SubElement(content, 'StorageClass')
        storage.text = 'STANDARD'

        owner = et.SubElement(content, 'Owner')

        owner_id = et.SubElement(owner, 'ID')
        owner_id.text = '123'

        owner_name = et.SubElement(owner, 'DisplayName')
        owner_name.text = '123'

    res = et.tostring(root)
    res = '<?xml version="1.0" encoding="UTF-8"?>'+res

    return res, 200

@blueprint.route('/<bucket>/<path:key>', methods=['GET'])
@authenticate
def get_key(bucket, key, user):
    """ Returns the bytes of a key.
    """
    return Response(blueprint.driver.key(bucket, key, user)), 200

@blueprint.errorhandler(InvalidAccessKeyId)
def handle_authentication_error(err):
    # TODO FIXME IMPLEMENT ME
    res = '<?xml version="1.0" encoding="UTF-8"?><Error><Code>InvalidAccessKeyId</Code></Error>'
    return res, 403

@blueprint.errorhandler(SignatureDoesNotMatch)
def handle_authentication_error(err):
    # TODO FIXME IMPLEMENT ME
    res = '<?xml version="1.0" encoding="UTF-8"?><Error><Code>SignatureDoesNotMatch</Code></Error>'
    return res, 403

@blueprint.errorhandler(AuthenticationError)
def handle_authentication_error(err):
    # TODO FIXME IMPLEMENT ME
    res = '<?xml version="1.0" encoding="UTF-8"?><Error><Code>AuthenticationError</Code></Error>'
    return res, 403

@blueprint.errorhandler(NoSuchBucketError)
def handle_bucket_lookup_error(err):
    # TODO FIXME IMPLEMENT ME
    res = '<?xml version="1.0" encoding="UTF-8"?><Error><Code>AuthenticationError</Code></Error>'
    return res, 404

@blueprint.errorhandler(NoSuchKeyError)
def handle_key_lookup_error(err):
    # TODO FIXME IMPLEMENT ME
    res = '<?xml version="1.0" encoding="UTF-8"?><Error><Code>AuthenticationError</Code></Error>'
    return res, 404

@blueprint.record
def get_config(setup):
    blueprint.driver = setup.app.config['flasks3']['driver']
