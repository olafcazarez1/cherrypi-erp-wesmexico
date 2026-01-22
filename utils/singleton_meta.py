from typing import Any


class MetaConfig(object):
    _instance = None

    __data = {}

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    def get_config(self, key: str, default: Any = None):
        """Getter data

        Args:

        Returns:
            string: scholarship id value

        Usage:
            >>> data = self.data
        """
        try:
            return self.__data[key]
        except AttributeError:
            return default

    def set_config(self, key, data):
        """Setter data

        Args:
            key(string): meta data key.
            data(any): meta data.

        Returns:

        Usage:
            >>> self.user_id = user_id
        """
        self.__data[key] = data

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.
        return cls._instance
