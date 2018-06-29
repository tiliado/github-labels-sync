# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from typing import List, Dict, Optional, Union

import requests

from github_labels_sync import graphql


DEFAULT_GRAPHQL_ENDPOINT_URL = 'https://api.github.com/graphql'


class GraphqlClient(graphql.Client):
    def __init__(self,
                 endpoint: str = DEFAULT_GRAPHQL_ENDPOINT_URL,
                 session: Optional[requests.Session] = None) -> None:
        super().__init__(endpoint, session)


class GitHub:
    graphql_client: graphql.Client

    def __init__(self, graphql_client: Optional[graphql.Client] = None) -> None:
        if not graphql_client:
            session = requests.Session()
            graphql_client = GraphqlClient(session=session)
        self.graphql_client = graphql_client

    def set_token(self, token: Union[bytes, str]) -> None:
        self.graphql_client.set_token(token)

    def unset_token(self) -> None:
        self.graphql_client.unset_token()

    def list_labels(self, repo: str) -> List[Dict[str, str]]:
        owner, repo = repo.split('/')
        data = self.graphql_client.query(
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
