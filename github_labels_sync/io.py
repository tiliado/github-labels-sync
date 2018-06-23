import os
from typing import Optional

DEFAULT_CONFIG_PATH = os.path.expanduser('~/.config')


def get_config_path(path: Optional[str] = None) -> str:
    return os.path.join(DEFAULT_CONFIG_PATH, path) if path else DEFAULT_CONFIG_PATH


DEFAULT_CONFIG_FILES = ['.github/labels.json', '.github_labels.json', 'labels.json']
DEFAULT_TOKEN_FILES = [get_config_path('github/oauth2_token.txt')]
