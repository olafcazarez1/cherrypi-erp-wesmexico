import datetime
import json
import re
from .exceptions import CustomHTTPException


class Validator:

	def validate_required(self, required: list, collection: dict) -> bool:
		"""Validate required fields

		Args:
			required (list): List of required fields
			collection (dict): Dict of fields to be validated

		Returns:
			True if the collection contains the required fields

		Raise:
			CustomHTTPException:
				400 - Arguments are required
		"""

		force = []
		clear_required = []
		for idx, arg in enumerate(required):
			# Required but could be empty
			if arg[0] in ['-', '+']:
				required[idx] = arg[1:]

			if arg[0] == '-':
				continue

			# Required and must have data
			force.append(
				arg if arg[0] == '+' else arg[1:]
			)

		req_args = set(required).difference(collection)
		if req_args:
			err = "Following arguments are required: {}"
			raise CustomHTTPException(400, err.format(", ".join(req_args)))
		return self.validate_not_empty(force, collection)

	def validate_not_empty(self, fields, collection: dict) -> bool:
		"""Validate parameters are empty (MUST NOT BE)

		Args:
			fields (list): List of required fields
			collection (dict): List of fields to be validated

		Returns:
			True if all fields are not empty in colletion

		Raise:
			CustomHTTPException:
				400 - Following arguments cannot be empty
		"""
		failed = []
		for field in fields:
			try:
				collection[field]
			except Exception:
				continue

			if collection[field] is None:
				failed.append(field)
				continue

			if isinstance(collection[field], str):
				if len(collection[field].strip()) <= 0:
					failed.append(field)
				continue

			if isinstance(collection[field], int):
				if len(str(collection[field]).strip()) <= 0:
					failed.append(field)
				continue

			if isinstance(collection[field], datetime.datetime):
				continue

			if len(str(collection[field])) <= 0:
				failed.append(field)

		if len(failed) > 0:
			msg = "Following arguments cannot be empty: {}"
			raise CustomHTTPException(400, msg.format(", ".join(failed)))
		return True

	def is_binary(self, value: str) -> bool:
		"""Validate if a value passed is a MySQL Binary
		Args:
			value (string): Value to be validated

		Returns:
			Boolean
		"""
		regex = re.compile("^[a-fA-F0-9]{32}$", re.I)
		return bool(regex.match(str(value)))

	def is_string(self, value: str) -> bool:
		"""Validate if an object is a string.

		Args:
			value (string): Value to be validated

		Returns:
			Boolean: True if string, otherwise False

		Usage:
		>>> is_string("foo") # returns true
		>>> is_string(b"foo") # returns false
		"""
		return isinstance(value, str)

	def is_full_string(self, value) -> bool:
		"""Validate if a string is not empty
			(it must contains at least one non space character).

		Args:
			value (string): Value to be validated

		Returns:
			Boolean: True if not empty, otherwise False

		Usage:
			>>> is_full_string(None) # returns false
			>>> is_full_string("") # returns false
			>>> is_full_string(" ") # returns false
			>>> is_full_string("hello") # returns true
		"""
		return self.is_string(value) and value.strip() != ""

	def is_number(self, value) -> bool:
		""" Checks if a string is a valid number.

		Args:
			value (string): Value to be validated

		Returns:
			Boolean: True if the string represents a number, false otherwise

		Usage:
			>>> is_number("42") # returns true
			>>> is_number("19.99") # returns true
			>>> is_number("-9.12") # returns true
			>>> is_number("1e3") # returns true
			>>> is_number("1 2 3") # returns false
		"""
		if not isinstance(value, str):
			msg = 'Expected "str", received "{}"'
			raise CustomHTTPException(400, msg.format(type(value)))

		regex = re.compile(r"^([+\-]?)((\d+)(\.\d+)?(e\d+)?|\.\d+)$")
		return regex.match(value) is not None

	def is_url(self, value) -> bool:
		""" Checks if a string is a valid url.

		Args:
			value (string): Value to be validated

		Returns:
			Boolean: True if url, false otherwise

		Usage:
			>>> is_url("http://www.mysite.com") # returns true
			>>> is_url("https://mysite.com") # returns true
			>>> is_url(".mysite.com") # returns false
		"""
		if not self.is_full_string(value):
			return False

		schemas = ["http", "https", "ftp"]
		regex = re.compile(
			r"^{}$".format((
				r"([a-z-]+://)"  # scheme
				r"([a-z_\d-]+:[a-z_\d-]+@)?"  # user:password
				r"(www\.)?"  # www.
				r"((?<!\.)[a-z\d]+[a-z\d.-]+\.[a-z]{2,6}|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|localhost)"
				r"(:\d{2,})?"  # port number
				r"(/[a-z\d_%+-]*)*"  # folders
				r"(\.[a-z\d_%+-]+)*"  # file extension
				r"(\?[a-z\d_+%-=]*)?"  # query string
				r"(#\S*)?"  # hash
			)),
			re.IGNORECASE,
		)

		valid = regex.match(value) is not None
		return valid and any([value.startswith(s) for s in schemas])

	def is_url_a_video(self, url: str) -> bool:
		"""Validate if a url is a video from youtube or vimeo

		Args:
			str: URL to be validated

		Returns:
			bool: True if the url is a youtube or vimeo link, False otherwise

		"""
		youtube = r'^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+$'
		vimeo = r'^(https?\:\/\/)?(www\.)?(vimeo\.com)\/.+$'
		if re.search(youtube, url):
			return True
		elif re.search(vimeo, url):
			return True
		return False

	def is_email(self, value) -> bool:
		""" Checks if a string is a valid email.

		Args:
			value (string): Value to be validated

		Returns:
			Boolean: True if email, false otherwise.

		Usage:
			>>> is_email("my.email@the-provider.com") # returns true
			>>> is_email("@gmail.com") # returns false
		"""
		if not self.is_full_string(value) or value.startswith("."):
			return False

		try:
			head, tail = value.split("@")
			if head.endswith(".") or (".." in head):
				return False
			head = head.replace("\\ ", "")
			if head.startswith('"') and head.endswith('"'):
				head = head.replace(" ", "")[1:-1]
			regex = re.compile(
				r"^{}$".format(
					r"[a-zA-Z\d._\+\-'`!%#$&*/=\?\^\{\}\|~\\]+@[a-z\d-]+\.?[a-z\d-]+\.[a-z]{2,4}"
				)
			)
			return regex.match(head + "@" + tail) is not None
		except ValueError:
			regex = re.compile(r'(?!"[^"]*)@+(?=[^"]*")|\\@')
			if regex.search(value) is not None:
				regex = re.compile(r'(?!"[^"]*)@+(?=[^"]*")|\\@')
				return self.is_email(regex.sub("a", value))
			return False

	def is_json(self, value) -> bool:
		""" Checks if a string is a valid json.

		Args:
			value (string): Value to be validated

		Returns:
			Boolean: True if json, false otherwise

		Usage:
			>>> is_json('{"name": "Peter"}') # returns true
			>>> is_json('[1, 2, 3]') # returns true
			>>> is_json('{nope}') # returns false
		"""
		regex = re.compile(
			r"^\s*[\[{]\s*(.*)\s*[\}\]]\s*$", re.MULTILINE | re.DOTALL
		)
		if self.is_full_string(value) and regex.match(value) is not None:
			try:
				return isinstance(json.loads(value), (dict, list))
			except(TypeError, ValueError, OverflowError):
				pass
		return False

	def is_uuid(self, value, allow_hex=False) -> bool:
		""" Checks if a string is a valid uuid.

		Args:
			value (string): Value to be validated

		Returns:
			Boolean: True if UUID, false otherwise

		Usage:
			>>> is_uuid("6f8aa2f9-686c-4ac3-8766-5712354a04cf") # returns true
			>>> is_uuid("6f8aa2f9686c4ac387665712354a04cf") # returns false
			>>> is_uuid(
					"6f8aa2f9686c4ac387665712354a04cf", allow_hex=True
				) # returns true
		"""
		s = str(value)
		regex = re.compile(
			r"^[a-f\d]{8}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{4}-[a-f\d]{12}$",
			re.IGNORECASE
		)
		if allow_hex:
			regex = re.compile(
				r"^[a-f\d]{32}$",
				re.IGNORECASE,
			)
			return regex.match(s) is not None
		return regex.match(s) is not None

	def is_md5(self, value) -> bool:
		""" Checks if a string is a valid md5.

		Args:
			value (string): Value to be validated

		Returns:
			Boolean: True if md5, false otherwise

		Usage:
			>>> is_md5("7815696ecbf1c96e6894b779456d330e") # returns true
			>>> is_md5("Hello world") # returns false
		"""
		s = str(value)
		regex = re.compile(
			r"^[a-fA-F\d]{32}$",
			re.IGNORECASE
		)
		return regex.match(s) is not None

	def is_zoom_id(self, value) -> bool:
		""" Checks if a string is a valid zoomcatalog identifier (Bigint)

		Args:
			value (string): Value to be validated

		Returns:
			Boolean: True if is a valid zoomcatalog id, false otherwise

		Usage:
			>>> is_zoom_id("1684184676568142474") # returns true
			>>> is_zoom_id("7815696ecbf1c96e6894b779456d330e") # returns false
		"""
		return re.match(r'[0-9]{18,}', str(value))
