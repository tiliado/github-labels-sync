# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from typing import Union, Any, Optional

import requests

from github_labels_sync.typing import StrDict


class Client:
    endpoint: str
    session: requests.Session
    headers: StrDict

    def __init__(self, endpoint: str, session: Optional[requests.Session] = None) -> None:
        self.endpoint = endpoint
        if not session:
            session = requests.Session()
        self.headers = {'Accept': 'application/json'}
        self.session = session

    def query(self, query: str, variables: Optional[dict] = None, **kwargs: Any) -> dict:
        if variables is None:
            variables = kwargs
        elif kwargs:
            variables.update(kwargs)

        response = self.session.post(self.endpoint, json={'query': query, 'variables': variables}, headers=self.headers)
        data = response.json()['data']
        assert isinstance(data, dict)
        return data

    __call__ = query

    def set_token(self, token: Union[bytes, str]) -> None:
        self.headers['Authorization'] = f'bearer {token if isinstance(token, str) else token.decode("ascii")}'

    def unset_token(self) -> None:
        del self.headers['Authorization']
