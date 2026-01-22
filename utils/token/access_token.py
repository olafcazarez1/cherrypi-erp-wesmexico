import uuid


class AccessToken:

    def __init__(self):
        pass

    @property
    def token_id(self):
        """Getter token_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> token_id = self.token_id
        """
        try:
            return self.__token_id
        except AttributeError:
            return None

    @token_id.setter
    def token_id(self, token_id):
        """Setter token_id

        Args:
                token_id(string): id.

        Returns:

        Usage:
                >>> self.token_id = token_id
        """
        self.__token_id = token_id

    @property
    def user_id(self):
        """Getter user_id

        Args:

        Returns:
                string: id value

        Usage:
                >>> user_id = self.user_id
        """
        try:
            return self.__user_id
        except AttributeError:
            return None

    @user_id.setter
    def user_id(self, user_id):
        """Setter user_id

        Args:
                user_id(string): id.

        Returns:

        Usage:
                >>> self.user_id = user_id
        """
        self.__user_id = user_id

    @property
    def is_valid(self):
        """Getter is_valid

        Args:

        Returns:
                boolen: status value

        Usage:
                >>> is_valid = self.is_valid
        """
        try:
            return self.__is_valid
        except AttributeError:
            return False

    @is_valid.setter
    def is_valid(self, is_valid):
        """Setter is_valid

        Args:
                is_valid(boolen): is token valid.

        Returns:

        Usage:
                >>> self.is_valid = is_valid
        """
        self.__is_valid = is_valid

    @property
    def version(self):
        """Getter version

        Args:

        Returns:
                string: id value

        Usage:
                >>> version = self.version
        """
        try:
            return self.__version
        except AttributeError:
            return None

    @version.setter
    def version(self, version):
        """Setter version

        Args:
                version(string): id.

        Returns:

        Usage:
                >>> self.version = version
        """
        self.__version = version

    @property
    def level(self):
        """Getter level

        Args:

        Returns:
                string: id value

        Usage:
                >>> level = self.level
        """
        try:
            return self.__level
        except AttributeError:
            return None

    @level.setter
    def level(self, level):
        """Setter level

        Args:
                level(string): id.

        Returns:

        Usage:
                >>> self.level = level
        """
        self.__level = level

    def __str__(self):
        return "{token_id}.{version}.{user_id}.{level}".format(
            token_id=self.token_id, version=self.version, user_id=self.user_id, level=self.level
        )

    def to_string(self):
        return AccessToken.generate(self.__token_id, self.__user_id, self.__version, self.__level)

    @classmethod
    def load(self, token, validate=True):
        try:
            tags = str(token).split(".")
            token = AccessToken()
            token.token_id = tags[0]
            token.version = tags[1]
            token.user_id = tags[2]
            token.level = tags[3]
            token.is_valid = True
        except (ValueError, KeyError) as e:
            raise e
        return token

    @classmethod
    def generate(cls, user_id, token_id=None, version="001", level="generic"):
        if token_id is None:
            token_id = str(uuid.uuid4())

        token = AccessToken()
        token.token_id = token_id
        token.version = version
        token.user_id = user_id
        token.level = level
        token.is_valid = True
        return token
