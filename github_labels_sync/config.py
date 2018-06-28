# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

import json
from typing import Optional, List

import os

from github_labels_sync import utils
from github_labels_sync.labels import Labels


class Config:
    path: str
    labels: Labels
    primary_repo: str
    secondary_repos: List[str]

    def __init__(self, path: str, *, primary_repo: Optional[str] = None, allow_empty: Optional[bool] = False) -> None:
        self.path = path
        data: dict = {}
        if os.path.isfile(path) or not allow_empty:
            with open(path) as fh:
                data = json.load(fh)
        mandatory = utils.get_str_dict_of_str_dicts(data, 'mandatory')
        optional = utils.get_str_dict_of_str_dicts(data, 'optional')
        aliases = utils.get_str_dict(data, 'aliases')
        self.labels = Labels(mandatory, optional, aliases)
        if not primary_repo:
            try:
                primary_repo = data['repos']['primary']
            except KeyError:
                primary_repo = None
        if not primary_repo:
            raise ValueError('No primary repository specified.')
        self.primary_repo = primary_repo
        try:
            self.secondary_repos = data['repos']['secondary'] or []
        except KeyError:
            self.secondary_repos = []

    def export(self) -> dict:
        self.secondary_repos.sort()
        return {
            '#mandatory': 'Labels that must be in each repository.',
            'mandatory': utils.sorted_dict(self.labels.mandatory),
            '#optional': 'Labels that may be in a repository.',
            'optional': utils.sorted_dict(self.labels.optional),
            '#aliases': 'Labels that must be renamed.',
            'aliases': utils.sorted_dict(self.labels.aliases),
            'repos': {
                '#primary': 'The repository to pull labels from.',
                'primary': self.primary_repo,
                '#secondary': 'Other repositories to push labels to.',
                'secondary': self.secondary_repos,
            }
        }

    def save(self, *, path: Optional[str] = None, force: Optional[bool] = False) -> bool:
        if force or self.labels.modified:
            if not path:
                path = self.path
            tmp_path = path + '~'
            directory = os.path.dirname(path)
            os.makedirs(directory, exist_ok=True)
            with open(tmp_path, 'wt') as fh:
                json.dump(self.export(), fh, indent=2, separators=(',', ': '))
            os.rename(tmp_path, path)
            self.labels.modified = False
            return True
        else:
            return False
