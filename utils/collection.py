import typing
from .exceptions import CustomHTTPException


class Collection:

	def __init__(self, cls: object) -> None:
		"""Constructor

		Args:
			cls (object): Class to be added in the collection
		"""
		self.objs = []
		self.cls = cls

	def add(self, obj: object) -> None:
		"""Add any object into a collection

		Raises:
			CustomHTTPException
				- 400: Invalid instance object in collection arguments
		"""
		if not isinstance(obj, self.cls):
			msg = "Invalid instance object in collection arguments"
			raise CustomHTTPException(400, msg)
		self.objs.append(obj)

	def one_or_none(self) -> typing.Optional[object]:
		"""Return the first element in the collection and in case

		Returns:
			typing.Optional[object]: First element or None
		"""
		return self.objs[0] if len(self.objs) > 0 else None

	def size(self) -> int:
		"""Return the size dimention of the collection

		Returns:
			int: Size of the collection
		"""
		return len(self.objs)

	def pop(self) -> typing.Optional[object]:
		"""Alias for one_or_none method

		Returns:
			typing.Optional[object]: First element or None
		"""
		return self.one_or_none()

	def all(self) -> list:
		"""Return all objects stored in the collection

		Returns:
			list: List of objects stored in the collection
		"""
		return self.objs

	def as_list(self, omitted: list = []) -> list:
		"""Return all objects stored in the collection

		Returns:
			list: List of objects as dict stored in the collection
		"""
		if not self.objs:
			return []
		objs = []
		for obj in self.objs:
			if omitted:
				objs.append(obj.as_dict(omitted=omitted))
			else:
				objs.append(obj.as_dict())
		return objs
