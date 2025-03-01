import abc
import urllib.parse
from typing import Any, Dict


class Middleware(metaclass=abc.ABCMeta):
    def __init__(self, app):
        self.app = app

    @abc.abstractmethod
    async def __call__(self, scope, receive, send):
        raise NotImplementedError()

    @classmethod
    def event_processor(cls, event, hint, asgi_scope) -> Dict[str, Any]:
        if asgi_scope['type'] in ('http', 'websocket'):
            event['request'] = {
                'url': cls.get_url(asgi_scope),
                'method': asgi_scope['method'],
                'headers': cls.get_headers(asgi_scope),
                'query_string': cls.get_query(asgi_scope),
            }
        if asgi_scope.get('client'):
            event['request']['env'] = {'REMOTE_ADDR': asgi_scope['client'][0]}
        if asgi_scope.get('endpoint'):
            event['transaction'] = cls.get_transaction(asgi_scope)
        return event

    @classmethod
    def get_url(cls, scope):
        """
        Extract URL from the ASGI scope, without also including the querystring.
        """
        scheme = scope.get('scheme', 'http')
        server = scope.get('server', None)
        path = scope.get('root_path', '') + scope['path']

        for key, value in scope['headers']:
            if key == b'host':
                host_header = value.decode('latin-1')
                return f'{scheme}://{host_header}{path}'

        if server is not None:
            host, port = server
            default_port = {
                'http': 80,
                'https': 443,
                'ws': 80,
                'wss': 443,
            }[scheme]
            if port != default_port:
                return f'{scheme}://{host}:{port}{path}'
            return f'{scheme}://{host}{path}'
        return path

    @staticmethod
    def get_query(scope):
        """
        Extract querystring from the ASGI scope,
        in the format that the Sentry protocol expects.
        """
        return urllib.parse.unquote(scope['query_string'].decode('latin-1'))

    @staticmethod
    def get_headers(scope):
        """
        Extract headers from the ASGI scope,
        in the format that the Sentry protocol expects.
        """
        headers = {}
        for raw_key, raw_value in scope['headers']:
            key = raw_key.decode('latin-1')
            value = raw_value.decode('latin-1')
            if key in headers:
                headers[key] = headers[key] + ', ' + value
            else:
                headers[key] = value
        return headers

    @staticmethod
    def get_transaction(scope):
        """
        Return a transaction string to identify the routed endpoint.
        """
        endpoint = scope['endpoint']
        qualname = (
            getattr(endpoint, '__qualname__', None)
            or getattr(endpoint, '__name__', None) or None
        )
        if not qualname:
            return None
        return f'{endpoint.__module__}.{qualname}'
