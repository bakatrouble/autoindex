from pathlib import Path

from environs import env

env.read_env()

BASE_HOSTS = env.list('BASE_HOSTS', default=['localhost:8000', '127.0.0.1:8000'])
DEBUG = env.bool('DEBUG', default=False)
FILES_DIR = Path(__file__).parent.parent / 'files'
SUBDOMAIN_FILES_DIR = Path(__file__).parent.parent / 'subdomain_files'
STATIC_DIR = Path(__file__).parent / '~static'

SORT_KEYS = {
    'name': lambda item: (not item.is_dir, item.name.lower()),
    '-name': lambda item: (item.is_dir, item.name.lower()),
    'size': lambda item: (not item.is_dir, item.size),
    '-size': lambda item: (item.is_dir, item.size),
    'created': lambda item: (not item.is_dir, item.created),
    '-created': lambda item: (item.is_dir, item.created),
}

ICONS = {
    'sort_asc': 'icon-up-dir',
    'sort_desc': 'icon-down-dir',
    'types': {
        'parent': 'icon-level-up',
        'dir': 'icon-folder',
        'file': 'icon-doc',
        'text': 'icon-doc-text',
        'image': 'icon-picture-outline',
        'music': 'icon-music-outline',
        'video': 'icon-video',
    },
}
