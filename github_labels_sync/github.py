# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from typing import List, Dict, Optional

import requests

from github_labels_sync import graphql


DEFAULT_ENDPOINT_URL = 'https://api.github.com/graphql'


class Client(graphql.Client):
    def __init__(self, endpoint: str = DEFAULT_ENDPOINT_URL, session: Optional[requests.Session] = None) -> None:
        super().__init__(endpoint, session)

    def list_labels(self, repo: str) -> List[Dict[str, str]]:
        owner, repo = repo.split('/')
        data = self.query(
            '''
            query ($owner: String!, $repo: String!) {
              repository(owner: $owner, name: $repo) {
                labels(first: 100) {
                  nodes {
                    id
                    name
                    color
                    description
                  }
                }
              }
            }
            ''', owner=owner, repo=repo)
        result: List[Dict[str, str]] = data['repository']['labels']['nodes']
        return result
