import sys

import flask

from flask import request

from .auth import authenticate
from .exceptions import AuthenticationError
from .exceptions import InvalidAccessKeyId
from .exceptions import SignatureDoesNotMatch


blueprint = flask.Blueprint('s3', __name__)
blueprint.config = dict()


@blueprint.route('/', methods=['GET'])
@authenticate
def get_service(user):
    """Return a list of buckets.
    """
    for bucket in blueprint.driver.buckets(user):
        print(bucket)
    # TODO FIXME IMPLEMENT ME
    res = '<?xml version="1.0" encoding="UTF-8"?><ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01"><Owner><ID>bcaf1ffd86f461ca5fb16fd081034f</ID><DisplayName>webfile</DisplayName></Owner><Buckets><Bucket><Name>bucket</Name><CreationDate>2006-02-03T16:45:09.000Z</CreationDate></Bucket><Bucket><Name>samples</Name><CreationDate>2006-02-03T16:41:58.000Z</CreationDate></Bucket></Buckets></ListAllMyBucketsResult>'
    return res, 200

@blueprint.route('/<bucket>/', methods=['GET'])
@authenticate
def get_bucket(bucket, user):
    """Returns a list of keys within a bucket.
    """
    for key in blueprint.driver.keys(bucket, user):
        print(key)
    # TODO FIXME IMPLEMENT ME
    res = '<?xml version="1.0" encoding="UTF-8"?><ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Name>bucket</Name><Prefix/><Marker/><MaxKeys>1000</MaxKeys><IsTruncated>false</IsTruncated><Contents><Key>my-image.jpg</Key><LastModified>2009-10-12T17:50:30.000Z</LastModified><ETag>&quot;fba9dede5f27731c9771645a39863328&quot;</ETag><Size>434234</Size><StorageClass>STANDARD</StorageClass><Owner><ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID><DisplayName>mtd@amazon.com</DisplayName></Owner></Contents><Contents><Key>my-third-image.jpg</Key><LastModified>2009-10-12T17:50:30.000Z</LastModified><ETag>&quot;1b2cf535f27731c974343645a3985328&quot;</ETag><Size>64994</Size><StorageClass>STANDARD_IA</StorageClass><Owner><ID>75aa57f09aa0c8caeab4f8c24e99d10f8e7faeebf76c078efc7c6caea54ba06a</ID><DisplayName>mtd@amazon.com</DisplayName></Owner></Contents></ListBucketResult>'
    return res, 200

@blueprint.route('/<bucket>/<path:key>', methods=['GET'])
@authenticate
def get_key(bucket, key, user):
    """Returns the bytes of a key.
    """
    # TODO FIXME IMPLEMENT ME
    return 'abc123', 200

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

@blueprint.record
def get_config(setup):
    blueprint.driver = setup.app.config['flasks3']['driver']
