# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from github_labels_sync.config import Config
from github_labels_sync.github import GitHub


def pull(github: GitHub, config: Config) -> int:
    owner, repo = config.primary_repo.split('/')
    labels = github.list_labels(config.primary_repo)
    config.labels.update(labels)
    config.save(force=True)
    for label in labels:
        print(github.get_label(owner, repo, label['name']))
    return 0
