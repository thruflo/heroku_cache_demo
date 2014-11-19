
import os
import requests
import tempfile
import time

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

PORT = int(os.environ.get('PORT', 5100))
DOWNLOAD_URL = u'http://static.thruflo.com/Large.pdf'

def download(url):
    r = requests.get(url, stream=True)
    f = tempfile.NamedTemporaryFile(delete=False)
    for chunk in r.iter_content(chunk_size=1024):
        if not chunk:
            continue
        f.write(chunk)
    f.close()
    return f.name

def handle(request):
    # Write 37MB to a unpredictably named temporary file.
    url = DOWNLOAD_URL
    filename = download(url)
    # Wait two seconds.
    time.sleep(2)
    # Delete the file.
    os.unlink(filename)
    # Return OK
    msg = u'Successfully downloaded\n{0}\nto\n{1}'.format(url, filename)
    return Response(msg)

if __name__ == '__main__':
    config = Configurator()
    config.add_route('index', '/')
    config.add_view(handle, route_name='index')
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()
