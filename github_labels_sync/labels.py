# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from typing import List, Optional, Iterable

from github_labels_sync.github import GitHub
from github_labels_sync.typing import StrDict, DictOfStrDicts


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
        raise NotImplementedError(repr(self))

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


PROPERTIES = 'color', 'description'


def find_changes(original: StrDict, changed: StrDict, properties: Iterable[str]) -> StrDict:
    changes: StrDict = {}
    for prop in properties:
        if original[prop] != changed[prop]:
            changes[prop] = changed[prop]
    return changes


class Labels:
    mandatory: DictOfStrDicts
    optional: DictOfStrDicts
    aliases: StrDict
    modified: bool

    def __init__(self,
                 mandatory: Optional[DictOfStrDicts] = None,
                 optional: Optional[DictOfStrDicts] = None,
                 aliases: Optional[StrDict] = None) -> None:
        self.mandatory: DictOfStrDicts = mandatory or {}
        self.optional: DictOfStrDicts = optional or {}
        self.aliases: StrDict = aliases or {}
        self.modified: bool = False

    def get_label(self, name: str) -> Optional[StrDict]:
        return self.mandatory.get(name, self.optional.get(name))

    def update(self, labels: List[StrDict]) -> None:
        for label in labels:
            name = label['name']
            if name not in self.aliases:
                item = self.optional.get(name, self.mandatory.get(name))
                if item:
                    for prop in PROPERTIES:
                        if item[prop] != label[prop]:
                            item[prop] = label[prop]
                            self.modified = True
                else:
                    self.mandatory[name] = {prop: label[prop] for prop in PROPERTIES}
                    self.modified = True

    def process(self, labels: List[StrDict]) -> List[Action]:
        actions: List[Action] = []
        labels_map: DictOfStrDicts = {}
        for label in labels:
            labels_map[label['name']] = label

        for name in tuple(labels_map.keys()):
            label = labels_map[name]
            if name in self.aliases:
                alias = self.aliases[name]
                if alias in labels_map:
                    actions.append(ReplaceAction(label, labels_map[alias]))
                else:
                    alias_label = self.get_label(alias)
                    assert alias_label
                    changes = find_changes(label, alias_label, PROPERTIES)
                    changes['name'] = alias
                    actions.append(RenameAction(label, changes))
                    labels_map[alias] = alias_label
                del labels_map[name]
            elif name not in self.mandatory and name not in self.optional:
                actions.append(UnknownLabelAction(label))

        for name, label in labels_map.items():
            item = self.get_label(name)
            if not item:
                continue
            updates = find_changes(label, item, PROPERTIES)
            if updates:
                actions.append(UpdateAction(label, updates))
        return actions
