from typing import List, Union, Optional

from github_labels_sync.typing import StrDict, DictOfStrDicts


class UpdateAction:
    def __init__(self, label: StrDict, updates: StrDict) -> None:
        self.updates = updates
        self.label = label


class ReplaceAction:
    def __init__(self, label: StrDict, replacement: StrDict) -> None:
        self.label = label
        self.replacement = replacement


class RenameAction:
    def __init__(self, label: StrDict, new_name: str) -> None:
        self.new_name = new_name
        self.label = label


Action = Union[UpdateAction, ReplaceAction, RenameAction]  # pylint: disable=invalid-name
PROPERTIES = 'color', 'description'


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
                    actions.append(RenameAction(label, alias))
                    labels_map[alias] = label
                del labels_map[name]
            elif name not in self.mandatory or name not in self.optional:
                raise ValueError('Unknown label "%s" - not in mandatory nor optional nor aliases.' % name)

        for name, label in labels_map.items():
            item = self.optional.get(name, self.mandatory.get(name))
            assert item
            updates = {}
            for prop in PROPERTIES:
                if item[prop] != label[prop]:
                    updates[prop] = item[prop]
            if updates:
                actions.append(UpdateAction(label, updates))
        return actions
