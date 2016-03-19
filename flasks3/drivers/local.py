import os

from .driver import S3StorageDriverABC

from .exceptions import NoSuchBucketError
from .exceptions import NoSuchKeyError


class LocalStorageDriver(S3StorageDriverABC):
    """ Local S3 storage driver.
    """
    def __init__(self, directory):
        self.directory = directory

    def buckets(self, user=None):
        """ Returns an iterable of buckets.
        """
        if user == 'mark':
            return (d for d in os.listdir(self.directory) if os.path.isdir(d))
        return []

    def keys(self, bucket, user=None):
        """ Returns an iterable of keys within a bucket.
        """
        root = os.path.join(self.directory, bucket)

        try: dirs = os.listdir(root)
        except OSError as err:
            raise NoSuchBucketError(bucket)

        for path, _, files in os.walk(root):
            for f in files:
                yield os.path.relpath(os.path.join(path, f), root)

    def key(self, bucket, key, user=None):
        """ Returns an iterable of bytes associated with the key.
        """
        path = os.path.join(self.directory, bucket, key)

        try: return open(path, 'rb')
        except IOError as err:
            raise NoSuchKeyError(key)
