# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from github_labels_sync.config import Config


def init(config: Config) -> int:
    config.save(force=True)
    return 0
