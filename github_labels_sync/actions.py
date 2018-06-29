# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from github_labels_sync.github import GitHub
from github_labels_sync.typing import StrDict


class Action:
    def run(self, github: GitHub, repo: str) -> None:
        raise NotImplementedError


class UpdateAction(Action):
    def __init__(self, label: StrDict, updates: StrDict) -> None:
        self.updates = updates
        self.label = label

    def run(self, github: GitHub, repo: str) -> None:
        github.update_label(repo, self.label["name"], self.updates)

    def __repr__(self) -> str:
        return f'Update: {self.label["name"]!r}'


class ReplaceAction(Action):
    def __init__(self, label: StrDict, replacement: StrDict) -> None:
        self.label = label
        self.replacement = replacement

    def run(self, github: GitHub, repo: str) -> None:
        old_label = self.label["name"]
        github.replace_label(repo, old_label, self.replacement["name"])
        github.delete_label(repo, old_label)

    def __repr__(self) -> str:
        return f'Replace: {self.label["name"]!r} → {self.replacement["name"]!r}'


class RenameAction(UpdateAction):
    def __repr__(self) -> str:
        return f'Rename: {self.label["name"]!r} → {self.updates["name"]!r}'


class UnknownLabelAction(Action):
    def __init__(self, label: StrDict) -> None:
        self.label = label

    def run(self, github: GitHub, repo: str) -> None:
        raise NotImplementedError(f'No idea what to do with {self.label["name"]!r} in {repo}')

    def __repr__(self) -> str:
        return f'Unknown: {self.label["name"]!r}'


class CreateAction(Action):
    def __init__(self, name: str, properties: StrDict, ) -> None:
        self.name = name
        self.properties = properties

    def run(self, github: GitHub, repo: str) -> None:
        github.create_label(repo, self.name, self.properties)

    def __repr__(self) -> str:
        return f'Create: {self.name!r}'
