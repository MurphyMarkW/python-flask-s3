import os

from .driver import S3StorageDriverABC


class LocalStorageDriver(S3StorageDriverABC):
    """ Local S3 storage driver.
    """
    def __init__(self, directory):
        self.directory = directory

    def buckets(self, user=None):
        """ Returns an iterable of buckets.
        """
        return (d[0] for d in os.walk(self.directory))

    def keys(self, bucket, user=None):
        """ Returns an iterable of keys within a bucket.
        """
        return (d[2] for d in os.walk(os.path.join(self.directory, bucket)))
