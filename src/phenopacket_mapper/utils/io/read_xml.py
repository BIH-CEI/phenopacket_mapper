from io import IOBase
from pathlib import Path
from typing import Union, Dict
import xmltodict


def read_xml(path: Union[str, Path, IOBase], encoding='utf-8') -> Dict:
    if isinstance(path, str):
        path = Path(path)

    if isinstance(path, Path):
        with open(path, 'r', encoding=encoding) as f:
            return parse_xml(f)
    elif isinstance(path, IOBase):
        return parse_xml(path)
    else:
        raise ValueError(f"Invalid input type {type(path)}.")


def _post_process_xml_dict(dict_: Dict) -> Dict:
    def parse_primitive_value(value: str):
        if value.isdigit():
            return int(value)
        elif value.lower() == "true":
            return True
        elif value.lower() == "false":
            return False
        else:
            try:
                return float(value)
            except ValueError:
                pass
        return value

    for k, v in dict_.items():
        print(f"{k=}, {type(k)=}, {v=}, {type(v)=}")
        if isinstance(v, dict):
            if v == {'@xsi:nil': 'true'}:  # resolves <null xsi:nil="true"/>
                dict_[k] = None
            else:
                dict_[k] = _post_process_xml_dict(v)
        elif isinstance(v, list):
            list_ = []
            print(f"{v=}")
            for i, item in enumerate(v):
                print(f"{item=}, {type(item)=}")
                if isinstance(item, dict):
                    list_.append(_post_process_xml_dict(item))
                else:
                    list_.append(parse_primitive_value(item))
            dict_[k] = list_
        elif isinstance(v, str):
            dict_[k] = parse_primitive_value(v)

    return dict_


def parse_xml(file: IOBase) -> Dict:
    """Parse an XML file into a dictionary with inferred types."""
    dict_ = xmltodict.parse(file.read())
    print(f"{dict_=}, {type(dict_)=}")
    dict_ = _post_process_xml_dict(dict_)
    return dict_

