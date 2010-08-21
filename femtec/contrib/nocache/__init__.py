import re

def _add_to_header(response, key, value):
    if response.has_header(key):
        values = re.split(r'\s*,\s*', response[key])
        if not value in values:
            response[key] = ', '.join(values + [value])
    else:
        response[key] = value

def _nocache_if_auth(request, response):
    if request.user.is_authenticated():
        _add_to_header(response, 'Cache-Control', 'no-store')
        _add_to_header(response, 'Cache-Control', 'no-cache')
        _add_to_header(response, 'Pragma', 'no-cache')
    return response

class NoCacheIfAuthenticatedMiddleware(object):
    def process_response(self, request, response):
        try:
            return _nocache_if_auth(request, response)
        except:
            return response

