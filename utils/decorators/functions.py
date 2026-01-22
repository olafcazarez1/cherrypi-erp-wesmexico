import inspect, logging, cherrypy

logger = logging.getLogger('internal.functions')

def check_arguments(callable, callable_args, callable_kwargs, self_included=False):
	'''Rip-off of the original function within cherrypy
	Done mostly to change 404s to 400s for missing query string and POST arguments
	Also, the original does not allow you to pass query string (kwargs) as regular arguments, unlike
	the actual dispatcher.

	Note this checker assumes an *explicit* URL mapping (not the cherrypy default), so always returns 400
	'''
	(args, varargs, varkw, defaults) = inspect.getargspec(callable)

	if args and args[0] == 'self' and not self_included:
		args =  args[1:]

	arg_usage = dict([(arg, 0,) for arg in args])
	vararg_usage = 0
	varkw_usage = 0
	extra_kwargs = set()

	for i, value in enumerate(callable_args):
		try:
			arg_usage[args[i]] += 1
		except IndexError:
			vararg_usage += 1

	for key in callable_kwargs.keys():
		try:
			arg_usage[key] += 1
		except KeyError:
			varkw_usage += 1
			extra_kwargs.add(key)

	for i, val in enumerate(defaults or []):
		# Defaults take effect only when the arg hasn't been used yet.
		if arg_usage[args[-i-1]] == 0:
			arg_usage[args[-i-1]] += 1

	missing_args = []
	multiple_args = []
	for key, usage in arg_usage.items():
		if usage == 0:
			missing_args.append(key)
		elif usage > 1:
			multiple_args.append(key)

	if missing_args:
		e = cherrypy.HTTPError(400,
				message="Missing parameters: %s" % ",".join(missing_args))
		logger.info('Client request malformed: %s' % e.args[1])
		raise e

	# the extra positional arguments come from the path - 404 Not Found
	if not varargs and vararg_usage > 0:
		e = cherrypy.HTTPError(400, 'Extra arguments found')
		logger.info('Client request malformed: %s' % e.args[1])
		raise e

	if multiple_args:
		e = cherrypy.HTTPError(400,
				message="Multiple values for parameters: "\
						"%s" % ",".join(multiple_args))
		logger.info('Client request malformed: %s' % e.args[1])
		raise e

	if not varkw and varkw_usage > 0:
		e = cherrypy.HTTPError(400,
			message="Unexpected parameters: %s" % ", ".join(extra_kwargs))
		logger.info('Client request malformed: %s' % e.args[1])
		raise e

def cors():
	if cherrypy.request.method == 'OPTIONS':
		cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
		cherrypy.response.headers["Access-Control-Allow-Headers"] = "Allow, Content-Type, Accept, X-Requested-With, Session, Authorization, Access-Token, Client-Identifier, Web-Site-Id"
		cherrypy.response.headers["Access-Control-Allow-Methods"] = "POST, PATCH, PUT, GET, DELETE, UPDATE, OPTIONS, HEAD"
		return True
	else:
		cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'
	return False