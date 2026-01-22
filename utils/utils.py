import cherrypy
import json
import uuid
import string


class Utils:

    def operators(self, op=None):
        """Convert logical string operators to logical operators

        Args:
            op (string, optional): String logical operator (Eg. 'lt', 'gt', 'eq', 'gte')

        Returns:
            string: Logical operator (E.g. <, >, =, >=) or list of operators

        """
        operators = {
            "lt": "<",
            "lte": "<=",
            "eq": "=",
            "gt": ">",
            "gte": ">=",
            "neq": "!=",
            "like": "LIKE",
            "in": "IN",
            "not in": "NOT IN",
        }
        if op:
            return operators.get(op, None)
        return operators

    def operator(self, op):
        """Convert logical string operators to logical operators

        Args:
            op (string),optional: String logical operator (Eg. 'lt', 'gt', 'eq', 'gte')

        Returns:
            string: Logical operator (E.g. <, >, =, >=)

        """
        return self.operators(op=op)

    def random_string(self, size=10, chars=string.ascii_lowercase + string.digits) -> str:
        """Generate random string

        Args:
            str: String of characters to use
            int: Length of the generated string

        Returns:
            str: Random string

        """
        return "".join([random.choice(chars) for _ in range(size)])

    # def generate_username(self, token: AccessToken, username: str) -> str:
    # 	"""Generate username based in token and username, if the application is
    # 	not part of the ZOOMcatalog services suite, then assume the user
    # 	belongs to a application linked to other company and the CLIENT_ID
    # 	is used as suffix

    # 	Args:
    # 		token (AccessToken): Acccess Token
    # 		username (str): Username

    # 	Returns:
    # 		str: Username
    # 	"""
    # 	if not isinstance(token, AccessToken):
    # 		raise CustomHTTPException(400, "Invalid token")

    # 	if not token.is_zoomcatalog:
    # 		username = "::".join([
    # 			username,
    # 			str(token.get_company_id())
    # 		])
    # 	return username

    # def clean_username(self, token: AccessToken, username: str) -> str:
    # 	"""Clean username based in token and username, if the application is
    # 	not part of the ZOOMcatalog services suite, then it only needs
    # 	to show the client_id otherwise username::client_id

    # 	Args:
    # 		token (AccessToken): Acccess Token
    # 		username (str): Username

    # 	Returns:
    # 		str: Username
    # 	"""
    # 	if not isinstance(token, AccessToken):
    # 		raise CustomHTTPException(400, "Invalid token")

    # 	if not token.is_zoomcatalog:
    # 		username = username.replace(
    # 			"::{}".format(token.get_client_id()), ""
    # 		)
    # 	return username

    # def add_url_param(self, url: str, params: dict) -> str:
    # 	"""Add query parameter in a url

    # 	Args:
    # 		url (str): URL to be edited
    # 		params (dict): Parameters to be added as query parameters

    # 	Returns:
    # 		str: A new url with query parameters
    # 	"""
    # 	from urllib.parse import urlparse, urlencode
    # 	url += ('&' if urlparse(url).query else '?') + urlencode(params)
    # 	return url

    def generate_uuid(self, dashes: bool = False) -> str:
        """GEnerate UUID

        Args:
            dashes (bool, optional): If true return uuid with dashes.
                Defaults to False.

        Returns:
            str: UUID
        """
        if dashes:
            return str(uuid.uuid4())
        return uuid.uuid4().hex

    # def encrypt_string(self, key: str, password: str,
    # 		is_password_md5: bool = False) -> str:
    # 	"""Encrypt password

    # 	Args:
    # 		key (str): String to be used as seed to encrypt
    # 		password (str): Password to be encrypted

    # 	Returns:
    # 		str: Password encrypted
    # 	"""
    # 	if not is_password_md5:
    # 		password = hashlib.md5(password.encode('utf-8')).hexdigest()
    # 	return Crypto_AES(
    # 		hashlib.sha1(
    # 			"{}*{}".format('zoom', key).encode('utf-8')
    # 		).hexdigest()
    # 	).encrypt(
    # 		password
    # 	)

    def clean_dict(self, dic: dict, lower: bool = False, upper: bool = False) -> str:
        """Apply some functions of every item in a dictionary

        Args:
            dic (dict): Dictionary to apply strip function

        Returns:
            dict: Cleaned dictionary
        """
        dic = {k: v.strip() if isinstance(v, str) else v for (k, v) in dic.items()}
        if lower:
            dic = {k: v.lower() if isinstance(v, str) else v for (k, v) in dic.items()}
        elif upper:
            dic = {k: v.upper() if isinstance(v, str) else v for (k, v) in dic.items()}
        return dic

    def remove_keys_from_dict(self, obj: dict, keys: list) -> dict:
        """Remove keys from a dictionary

        Args:
            obj (dict): Dict to remove values
            keys (list): List of keys to remove from the dict

        Returns:
            dict: Cleaned dictionary
        """
        for k in keys:
            try:
                del obj[k]
            except KeyError:
                pass
        return obj

    def keep_keys_from_dict(self, obj: dict, keys: list) -> dict:
        response = {}
        for k, v in obj.items():
            for kk in keys:
                if k == kk:
                    response[k] = v
                    break
        return response

    def convert_filters(self, filters: dict, ignore: list = [], force_status: bool = False) -> list:
        criterias = []

        try:
            """Insert the phases"""
            items = json.loads(filters)
        except Exception:
            raise cherrypy.HTTPError(400, "Incorrect format/value for `filters`")

        # Process Specific Filters
        has_status = False
        for item in items:
            if item["value"] is None:
                continue
            if item["filter_by"] in ignore:
                continue

            if item["filter_by"] == "status":
                has_status = True

                if "+" in item["value"]:
                    item["value"] = item["value"].split("+")
                    item["operator"] = "in"

            criterias.append({item["filter_by"]: item["value"], "op": item["operator"]})

        if has_status == False and force_status:
            criterias.append({"status": "active", "op": "eq"})

        return criterias

    def get_filter(self, filters: dict, key: str) -> dict:
        try:
            """Insert the phases"""
            items = json.loads(filters)
        except Exception:
            raise cherrypy.HTTPError(400, "Incorrect format/value for `filters`")

        for item in items:
            if item["filter_by"] != key:
                continue

            if item["value"] is None:
                continue

            return {item["filter_by"]: item["value"], "op": item["operator"]}

        return None
