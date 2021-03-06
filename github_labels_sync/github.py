# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from typing import List, Dict, Optional, Union, Iterable, Any

import requests

from github_labels_sync import graphql, rest

DEFAULT_GRAPHQL_ENDPOINT_URL = 'https://api.github.com/graphql'
DEFAULT_REST_ENDPOINT_URL = 'https://api.github.com'


class GraphqlClient(graphql.Client):
    def __init__(self,
                 endpoint: str = DEFAULT_GRAPHQL_ENDPOINT_URL,
                 session: Optional[requests.Session] = None) -> None:
        super().__init__(endpoint, session)


class RestClient(rest.Client):
    def __init__(self,
                 endpoint: str = DEFAULT_REST_ENDPOINT_URL,
                 session: Optional[requests.Session] = None) -> None:
        super().__init__(endpoint, session)
        self.headers['Accept'] = 'application/vnd.github.symmetra-preview+json'


class GitHub:
    graphql_client: graphql.Client
    rest_client: rest.Client

    def __init__(self,
                 graphql_client: Optional[graphql.Client] = None,
                 rest_client: Optional[rest.Client] = None) -> None:
        if not graphql_client or not rest_client:
            session = requests.Session()
            if not graphql_client:
                graphql_client = GraphqlClient(session=session)
            if not rest_client:
                rest_client = RestClient(session=session)
        self.graphql_client = graphql_client
        self.rest_client = rest_client

    def set_token(self, token: Union[bytes, str]) -> None:
        self.graphql_client.set_token(token)
        self.rest_client.set_token(token)

    def unset_token(self) -> None:
        self.graphql_client.unset_token()
        self.rest_client.unset_token()

    def get_label(self, owner: str, repo: str, name: str) -> dict:
        result = self.rest_client(f'/repos/{owner}/{repo}/labels/{name}')
        assert isinstance(result, dict)
        return result

    def create_label(self, repo: str, name: str, properties: dict) -> dict:
        properties['name'] = name
        result = self.rest_client.post(f'/repos/{repo}/labels', properties)
        assert isinstance(result, dict)
        return result

    def update_label(self, repo: str, name: str, properties: dict) -> dict:
        result = self.rest_client.patch(f'/repos/{repo}/labels/{name}', properties)
        assert isinstance(result, dict)
        return result

    def delete_label(self, repo: str, name: str) -> None:
        self.rest_client.delete(f'/repos/{repo}/labels/{name}')

    def replace_label(self, repo: str, old_label: str, new_label: str) -> None:
        while True:
            issues = self.list_issues_with_label(repo, old_label)
            if not issues:
                break
            for issue in issues:
                number: int = issue['number']
                self.add_label_to_issue(repo, number, new_label)
                self.remove_label_from_issue(repo, number, old_label)

    def add_label_to_issue(self, repo: str, issue: int, label: str) -> List[str]:
        return self.add_labels_to_issue(repo, issue, [label])

    def add_labels_to_issue(self, repo: str, issue: int, labels: Iterable[str]) -> List[str]:
        result = self.rest_client.post(f'/repos/{repo}/issues/{issue}/labels', list(labels))
        assert isinstance(result, list)
        return result

    def remove_label_from_issue(self, repo: str, issue: int, label: str) -> None:
        self.rest_client.delete(f'/repos/{repo}/issues/{issue}/labels/{label}')

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

    def list_issues_with_label(self, repo: str, label: str) -> List[Dict[str, Any]]:
        owner, repo = repo.split('/')
        data = self.graphql_client.query(
            '''
            query ($owner: String!, $repo: String!, $label: String!) {
              repository(owner: $owner, name: $repo) {
                issues(labels: [$label], first: 100) {
                  nodes {
                    number
                  }
                }
              }
            }
            ''', owner=owner, repo=repo, label=label)
        result: List[Dict[str, str]] = data['repository']['issues']['nodes']
        return result
