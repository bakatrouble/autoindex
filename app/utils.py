from dataclasses import dataclass
from datetime import datetime
from mimetypes import guess_type
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

from conf import BASE_HOSTS, SORT_KEYS, ICONS, FILES_DIR, SUBDOMAIN_FILES_DIR


def icon_html(cls):
    return f'<i class="{cls}"></i>'


@dataclass
class ListEntry:
    name: str
    mime: str | None
    is_dir: bool
    size: int
    created: float

    def __init__(self, path: Path):
        self.name = path.name
        self.mime = guess_type(self.name)[0]
        self.is_dir = path.is_dir()
        self.size = path.stat().st_size
        self.created = path.stat().st_ctime

    @property
    def link_name(self):
        if self.is_dir:
            return f'{self.name}/'
        return self.name

    @property
    def display_name(self):
        if self.is_dir:
            return f'{self.name}/'
        return f'{self.name} [{self.mime}]'

    @property
    def icon(self):
        if self.name == '..':
            return icon_html(ICONS['types']['parent'])
        elif self.is_dir:
            return icon_html(ICONS['types']['dir'])
        elif self.mime:
            t = self.mime.split('/')[0]
            if t in ICONS['types']:
                return icon_html(ICONS['types'][t])
        return icon_html(ICONS['types']['file'])

    @property
    def formatted_date(self):
        return datetime.fromtimestamp(self.created).strftime('%Y-%m-%d %H:%M:%S')

    @property
    def formatted_size(self):
        size = self.size
        for unit in ['B', 'KiB', 'MiB', 'GiB', 'TiB']:
            if size < 2048:
                return f'{size} {unit}'
            else:
                size //= 1024
        return f'{size} PiB'


def get_j2env(debug=False):
    return Environment(loader=FileSystemLoader([Path(__file__).parent.absolute()]),
                       trim_blocks=True, optimized=debug, cache_size=0 if debug else 400)


def get_sort_icon(test, sort):
    if sort == test:
        return icon_html(ICONS['sort_asc'])
    elif sort == f'-{test}':
        return icon_html(ICONS['sort_desc'])
    else:
        return ''


def get_sort_link(current, sort, hidden):
    return f'?sort={"-" if current == sort else ""}{sort}{"&hidden" if hidden else ""}'


def resolve_path(domain, path):
    path_parts = [i for i in path.split('/') if i not in ['.', '..']]
    joined_parts = '/'.join(path_parts)
    if domain in BASE_HOSTS:
        return FILES_DIR.joinpath(*path_parts), joined_parts
    else:
        for host in BASE_HOSTS:
            if host in domain:
                return SUBDOMAIN_FILES_DIR.joinpath(domain[:domain.index(host) - 1], *path_parts), joined_parts

    raise ValueError()


def list_dir(directory: Path, sort, hidden=False, root=True):
    lst = [ListEntry(path) for path in directory.iterdir() if hidden or not path.name.startswith('.')]
    lst = sorted(lst, key=SORT_KEYS[sort], reverse=sort.startswith('-'))
    if not root:
        lst = [ListEntry(Path('..'))] + lst
    return lst
