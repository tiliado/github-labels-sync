# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from typing import Union

from github_labels_sync import http


class Client(http.Client):
    def set_token(self, token: Union[bytes, str]) -> None:
        self.headers['Authorization'] = f'bearer {token if isinstance(token, str) else token.decode("ascii")}'

    def unset_token(self) -> None:
        del self.headers['Authorization']

    def call(self, method: str) -> Union[dict, list]:
        response = self.session.get(f'{self.endpoint}{method}', headers=self.headers)
        data = response.json()
        assert isinstance(data, (dict, list))
        return data

    def post(self, method: str, data: Union[dict, list]) -> Union[dict, list]:
        response = self.session.post(f'{self.endpoint}{method}', headers=self.headers, json=data)
        data = response.json()
        assert isinstance(data, (dict, list))
        return data

    def patch(self, method: str, data: Union[dict, list]) -> Union[dict, list]:
        response = self.session.patch(f'{self.endpoint}{method}', headers=self.headers, json=data)
        data = response.json()
        assert isinstance(data, (dict, list))
        return data

    def delete(self, method: str) -> None:
        self.session.delete(f'{self.endpoint}{method}', headers=self.headers)

    __call__ = call
