from typing import Dict

import requests


def get(url: str, params: Dict = None, json=False):
    if params:
        r = requests.get(url=url, params=params)
    else:
        r = requests.get(url=url)

    if json:
        return r.json()
    else:
        return r.text