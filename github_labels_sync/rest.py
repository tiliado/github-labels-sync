# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from typing import Union

from github_labels_sync import http


class Client(http.Client):
    def set_token(self, token: Union[bytes, str]) -> None:
        self.headers['Authorization'] = f'bearer {token if isinstance(token, str) else token.decode("ascii")}'

    def unset_token(self) -> None:
        del self.headers['Authorization']

    def call(self, method: str) -> dict:
        response = self.session.get(f'{self.endpoint}{method}', headers=self.headers)
        data = response.json()
        assert isinstance(data, dict)
        return data

    __call__ = call