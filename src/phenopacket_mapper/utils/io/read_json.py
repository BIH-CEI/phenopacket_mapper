import json
from io import IOBase
from pathlib import Path
from typing import Union, Dict


def read_json(path: Union[str, Path, IOBase]) -> Dict:
    if isinstance(path, str):
        path = Path(path)

    if isinstance(path, Path):
        f = open(path)
    elif isinstance(path, IOBase):
        f = path
    else:
        raise ValueError(f"Invalid input type {type(path)}.")

    return json.load(f)