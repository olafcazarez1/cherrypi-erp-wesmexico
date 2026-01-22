from __future__ import annotations


class CustomHTTPException(Exception):
	"""
	HTTP Custom exception to catch it in request output decorator and send the
	corresponding http headers and http code
	"""

	def __init__(self, code: int, msg: str, *args) -> None:
		"""Constructor

		Args:
			code (int): Error code
			msg (str): Error message
		"""
		self.code, self.msg = code, msg
		super(CustomHTTPException, self).__init__(code, msg, *args)


class DatabaseException(Exception):
	"""
	Database Exception to catch it in request output decorator and send the
	corresponding http headers and http code
	"""

	def __init__(self, code: int, msg: str, *args) -> None:
		"""Constructor

		Args:
			code (int): Error code
			msg (str): Error message
		"""
		self.code, self.msg = code, msg
		super(DatabaseException, self).__init__(code, msg, *args)
