# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

import argparse
from typing import List, Optional
import os

from github_labels_sync import io
from github_labels_sync.config import Config
from github_labels_sync.github import GitHub
from github_labels_sync.init_command import init
from github_labels_sync.pull_command import pull
from github_labels_sync.push_command import push


def main(argv: List[str]) -> Optional[int]:
    parser = argparse.ArgumentParser(prog=argv[0], description='Synchronize GitHub labels.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--init', action='store_true', default=False,
                       help='Initialize empty configuration file.')
    group.add_argument('--pull', action='store_true', default=False,
                       help='Pull labels from primary repository and update local labels configuration.')
    group.add_argument('--push', action='store_true', default=False,
                       help='Push labels from local configuration to all repositories.')
    parser.add_argument('--primary-repo',
                        help='Set primary repository, overriding that in configuration file.')
    parser.add_argument('--config',
                        help='Set path to configuration file.')
    parser.add_argument('--dir',
                        help='Change working directory at the very beginning.')
    parser.add_argument('--dry-run',
                        help='Only print what actions would be performed.')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--token',
                       help='Set GitHub OAuth2 token.')
    group.add_argument('--token-file',
                       help='Set file to load the GitHub OAuth2 token from.')
    params = parser.parse_args(argv[1:])

    if params.dir:
        os.chdir(params.dir)

    config = load_config(params)
    if params.init:
        return init(config)

    token = load_token(params)

    github = GitHub()
    github.set_token(token)
    if params.pull:
        return pull(github, config)
    if params.push:
        return push(github, config)
    raise Exception('Unknown action')


def load_config(params: argparse.Namespace) -> Config:
    config_path = params.config
    if not config_path:
        for config_path in io.DEFAULT_CONFIG_FILES:
            if os.path.isfile(config_path):
                break
        else:
            if params.init:
                config_path = io.DEFAULT_CONFIG_FILES[0]
            else:
                raise ValueError(
                    f'Cannot find config file. Tried: {", ".join(repr(s) for s in io.DEFAULT_CONFIG_FILES)}')

    return Config(config_path, primary_repo=params.primary_repo, allow_empty=params.init)


def load_token(params: argparse.Namespace) -> str:
    token: Optional[str] = params.token.strip() if params.token else None
    if not token:
        token_path = params.token_file
        if not token_path:
            for token_path in io.DEFAULT_TOKEN_FILES:
                if os.path.isfile(token_path):
                    break
            else:
                raise ValueError(f'Cannot find token file. Tried: {", ".join(repr(s) for s in io.DEFAULT_TOKEN_FILES)}')
        with open(token_path) as fh:
            token = fh.read().strip()
    if not token:
        raise ValueError('You need OAuth2 token.')
    return token
