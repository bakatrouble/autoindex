import os
import socket
from os import environ
from pathlib import Path

from sanic import Sanic
from sanic.request import Request
from sanic.response import text, html, file_stream, redirect
from sanic.exceptions import abort

from utils import get_j2env, get_sort_icon, get_sort_link, resolve_path, list_dir


DEBUG = environ.get('ENV', '').upper() != 'PRODUCTION'

app = Sanic()
app.static('/~static/', '~static/', use_content_range=True, stream_large_files=True)
j2env = get_j2env(DEBUG)


@app.route('/')
@app.route('/<path:path>')
async def index(request: Request, path=''):
    domain = request.host
    query = f'?{request.query_string}' if request.query_string else ''

    try:
        resolved_path, resolved_query = resolve_path(domain, path)
    except ValueError:
        return text('GTFO', 400)

    if resolved_path.is_dir():
        if path and path[-1] != '/':
            return redirect(f'/{path}/')

        hidden = request.args.get('hidden') is not None
        sort = request.args.get('sort', 'name')
        if sort not in ['name', '-name', 'size', '-size', 'created', '-created']:
            sort = 'name'

        return html(j2env.get_template('filelist.tpl').render(
            lst=list_dir(resolved_path, sort, hidden, root=not resolved_query),
            get_sort_icon=get_sort_icon,
            get_sort_link=get_sort_link,
            sort=sort,
            hidden=hidden,
            path=resolved_query,
            query=query,
        ))
    elif resolved_path.is_file():
        return await file_stream(resolved_path)

    abort(404, 'Path was not found')


if __name__ == '__main__':
    if DEBUG:
        app.run(host='localhost', port=8080, debug=True, auto_reload=True)
    else:
        socket_address = Path('/tmp/drop.sock')
        try:
            socket_address.unlink()
        except OSError:
            if socket_address.exists():
                raise

        sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        sock.bind(str(socket_address))
        socket_address.chmod(0o666)
        app.run(sock=sock, workers=2)
