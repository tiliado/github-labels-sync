# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from github_labels_sync.config import Config
from github_labels_sync.github import GitHub
from github_labels_sync.actions import UnknownLabelAction


def push(github: GitHub, config: Config) -> int:
    all_ok: bool = True
    for repo in config.all_repos:
        labels = github.list_labels(repo)
        actions = config.labels.process(labels)
        proceed: bool = True
        for action in actions:
            if isinstance(action, UnknownLabelAction):
                print(repo, 'Error:', action)
                proceed = False
        if not proceed:
            print(repo, '→ Aborting because of errors.')
            all_ok = False
            break

        for action in actions:
            print(repo, action)
            action.run(github, repo)
    return 0 if all_ok else 1
