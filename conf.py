BASE_HOSTS = [
    'drop.bakatrouble.pw',
    'drop.bakatrouble.me',
    'drop.home.bakatrouble.me',
    '127.0.0.1.xip.io:8080',
    'localhost:8080',
]

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
