import json, cherrypy
import simplejson
import zlib
import base64

from functools import wraps
from typing import Callable

from utils.decorators import functions
from utils.token.access_token import AccessToken
from utils.exceptions import CustomHTTPException
from utils.validator import Validator

def validate_body_params(fields: list = [],
			exception: bool = True) -> Callable:
	"""Decorator to validate HTTP body parameters, this one should be used
	with request_output to handle correctly the response output

	Args:
		fields (list, optional): [description]. Defaults to [].
		exception (bool, optional): [description]. Defaults to True.

	Raises:
		CustomHTTPException
			- 400: Invalid HTTP JSON Body

	Returns:
		Callable: function to continue execution

	Usage:
		from utils import decorators
		from utils.decoratos.tools import (
			validate_body_params
		)
		@request_output
		@validate_body_params(['param1', 'param2'])
		def func():
			pass
	"""
	def callable(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			try:
				body = cherrypy.request.json
			except Exception:
				raise cherrypy.HTTPError(
					400, 
					'Invalid HTTP JSON Body'
				)
			try:
				Validator().validate_required(fields, body)
			except CustomHTTPException as e:
				if exception:
					raise cherrypy.HTTPError(
						e.code, 
						e.msg
					)
			return f(*args, **kwargs)
		return wrapped
	return callable

def jsonify(fn):
	@wraps(fn)
	def wrapped(*args, **kw):
		try:
			functions.check_arguments(fn, args, kw, True)
			result = fn( *args, **kw)
			# result = unicode(result, 'utf-8')
		except TypeError as err:
			raise cherrypy.HTTPError(400, str(err))

		cherrypy.response.headers['Content-Type'] = 'application/json;charset=utf-8;'
		return json.dumps(result, ensure_ascii=True)
	return wrapped

def simple_jsonify(fn):
	@wraps(fn)
	def wrapped(*args, **kw):
		try:
			functions.check_arguments(fn, args, kw, True)
			result = fn( *args, **kw)
		except TypeError as err:
			raise cherrypy.HTTPError(
				400, 
				str(err)
			)

		cherrypy.response.headers['Content-Type'] = 'application/json;charset=utf-8;'
		return simplejson.dumps(result, ensure_ascii=True)

	return wrapped

def zip_compression(fn):
	@wraps(fn)
	def wrapped(*args, **kw):
		cherrypy.response.headers['Content-Type'] = 'text/plain;charset=utf-8;'
		cherrypy.response.headers['Content-Encoding'] = 'base64'
		return base64.b64encode(zlib.compress(fn( *args, **kw)))
	return wrapped

def secured(access_levels: list = None) -> Callable:
	"""Decorator to validate the access or user token send to the HTTP request
	in the Authorization HTTP header.

	Args:

	Raises:
		HTTPError
			- 500: Invalid rsa parameter in secured decorator
			- 401: Invalid access token received
			- 403: Authorization header is required

	Returns:
		Callable: decorated_function(func)

		# Validate the access token is comming in the HTTP headers
		# and the token is valid and contains the scope 'app:read'
		@secured()
		def func():
			pass
	"""
	def callable(f):
		@wraps(f)
		def wrapped(*args, **kwargs):
			if not cherrypy.request.headers.get("Authorization", None):
				msg = 'Authorization header is required'
				raise cherrypy.HTTPError(403, msg)
			try:
				token = AccessToken.load(
					token=cherrypy.request.headers.get('Authorization'),
					validate=True
				)
			except Exception as e:
				raise cherrypy.HTTPError(500, e.msg)

			if not token.is_valid:
				msg = 'Unauthorized'
				raise cherrypy.HTTPError(401, msg)

			if access_levels and token.level not in access_levels:
				msg = 'Unauthorized'
				raise cherrypy.HTTPError(403, msg)

			kwargs['token'] = token
			return f(*args, **kwargs)
		return wrapped
	return callable



def cors(fn):
	@wraps(fn)
	def wrapped(*args, **kw):
		if functions.cors():
			return str(True)
		return fn( *args, **kw)
	return wrapped
