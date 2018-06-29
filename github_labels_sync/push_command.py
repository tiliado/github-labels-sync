# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from github_labels_sync.config import Config
from github_labels_sync.github import GitHub


def push(github: GitHub, config: Config) -> int:
    print("Push not implemented yet.", github, config)
    return 1
