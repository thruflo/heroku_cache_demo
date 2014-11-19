
import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

PORT = int(os.environ.get('PORT', 8080))

def index(request):
    return Response('Hello %(name)s!' % request.matchdict)

if __name__ == '__main__':
    config = Configurator()
    config.add_route('index', '/')
    config.add_view(index, route_name='index')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()
