# Copyright 2018 Jiří Janoušek <janousek.jiri@gmail.com>
# Licensed under BSD-2-Clause license - see file LICENSE for details.

from typing import Optional

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
