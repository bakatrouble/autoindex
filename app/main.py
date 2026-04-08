from pathlib import Path

from sanic import Sanic, HTTPResponse
from sanic.request import Request
from sanic.response import text, html, file_stream, redirect
from sanic.exceptions import NotFound, MethodNotAllowed
from sanic_cors import CORS
from sanic_ext import Extend

from conf import STATIC_DIR
from utils import get_j2env, get_sort_icon, get_sort_link, resolve_path, list_dir


DEBUG = Path('.debug').exists()

app = Sanic('autoindex', strict_slashes=True)
Extend(app)
cors = CORS(app)
app.static('/~static/', STATIC_DIR, use_content_range=True, stream_large_files=True)
print(STATIC_DIR)
j2env = get_j2env(DEBUG)


@app.get(r'/<path:.*/?>')
async def index(request: Request, path=''):
    path = path.replace('%20', ' ')
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
        stream = await file_stream(resolved_path)
        if request.method == 'HEAD':
            stream.headers['Content-Length'] = resolved_path.stat().st_size
            return HTTPResponse(
                '', status=200, headers=stream.headers, content_type=stream.content_type
            )
        return stream

    raise NotFound('Path was not found')


if __name__ == '__main__':
    if DEBUG:
        app.run(host='0.0.0.0', port=8000, debug=True, auto_reload=True)
    else:
        app.run(host='::', port=8000, workers=4)
