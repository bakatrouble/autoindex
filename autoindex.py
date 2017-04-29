from bottle import route, request, run, redirect, template, default_app, abort
import os
from datetime import datetime
from mimetypes import guess_type

base_hosts = [
    'drop.217.182.90.36.xip.io'
]


def format_size(size):
    for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
        if size < 2048:
            return f'{size} {unit}'
        else:
            size //= 1024
    return f'{size} PiB'


def format_date(ts):
    return datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')


def get_sort_icon(test, sort):
    if sort == test:
        return '<i class="sort descending icon"></i>'
    elif sort == f'-{test}':
        return '<i class="sort ascending icon"></i>'
    else:
        return ''


def get_sort_link(current, sort, hidden):
    return f'?sort={"-" if current == sort else ""}{sort}{"&hidden" if hidden else ""}'


def get_file_icon(name):
    mime = guess_type(name)[0]
    if mime:
        t = mime.split('/')[0]
        if t in ['text', 'image', 'audio', 'video']:
            return t
    return ''


class ListEntry:
    def __init__(self, dir, name):
        path = os.path.join(dir, name)
        self.name = name
        self.isdir = os.path.isdir(path)
        self.size = os.path.getsize(path)
        self.created = os.path.getctime(path)


def resolve_path(domain, path):
    if domain in base_hosts:
        return os.path.join(os.path.dirname(__file__), 'files', *path.split('/'))
    else:
        for host in base_hosts:
            if host in domain:
                return os.path.join(os.path.dirname(__file__), 'subdomain_files',
                                    domain[:domain.index(host)-1], *path.split('/'))
    raise ValueError


def list_dir(dir, sort=None, hidden=False):
    lst = [ListEntry(dir, name) for name in os.listdir(dir) if hidden or not name.startswith('.')]
    lst = sorted(lst, key={
        'name': lambda item: (not item.isdir, item.name.lower()),
        '-name': lambda item: (item.isdir, item.name.lower()),
        'size': lambda item: (not item.isdir, item.size),
        '-size': lambda item: (item.isdir, item.size),
        'created': lambda item: (not item.isdir, item.created),
        '-created': lambda item: (item.isdir, item.created)
    }[sort], reverse=sort.startswith('-'))
    return lst


@route('/')
@route('/<path:path>')
def index(path=''):
    domain = request.urlparts.netloc
    query = request.urlparts.query
    try:
        resolved_path = resolve_path(domain, path)
    except ValueError:
        return 'GTFO'
    if os.path.isdir(resolved_path):
        if path and path[-1] != '/':
            return redirect(f'/{path}/')

        hidden = 'hidden' in request.GET
        sort = request.GET.get('sort', 'name')
        if sort not in ['name', '-name', 'size', '-size', 'created', '-created']:
            sort = 'name'

        return template('filelist',
                        lst=list_dir(resolved_path, sort, hidden),
                        format_size=format_size,
                        format_date=format_date,
                        get_sort_icon=get_sort_icon,
                        get_sort_link=get_sort_link,
                        sort=sort,
                        hidden=hidden,
                        path=path,
                        query=query,
                        guess_type=guess_type,
                        get_file_icon=get_file_icon)
    else:
        return abort(404)

application = default_app()

if __name__ == '__main__':
    run(host='localhost', port=8080, debug=True, reloader=True)
