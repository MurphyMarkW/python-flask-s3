import abc


class S3StorageDriverABC(object):
    """S3 Storage driver abstract base class.

    Defines interfaces for any S3-compatible storage backend.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def buckets(self, user=None):
        """Returns an iterable of buckets.
        """
        raise NotImplementedError('TODO')

    @abc.abstractmethod
    def keys(self, bucket, user=None):
        """Returns an iterable of keys within a bucket.
        """
        raise NotImplementedError('TODO')
