from typing import Dict, List


def recursive_dict_call(d: Dict, keys: List, default=None):
    if not isinstance(d, dict):
        return d
    elif len(keys) == 1:
        return d.get(keys[0], default)
    else:
        return recursive_dict_call(d.get(keys[0], default), keys[1:])