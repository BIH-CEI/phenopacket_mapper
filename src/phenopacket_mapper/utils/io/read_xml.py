from io import IOBase
from pathlib import Path
from typing import Union, Dict
from xml.etree import ElementTree


def read_xml(path: Union[str, Path, IOBase]) -> Dict:
    if isinstance(path, str):
        path = Path(path)

    if isinstance(path, Path):
        f = open(path)
    elif isinstance(path, IOBase):
        f = path
    else:
        raise ValueError(f"Invalid input type {type(path)}.")

    tree = ElementTree.parse(f)
    root = tree.getroot()

    return parse_xml_element(root)


def parse_xml_element(element):
    """Parse an XML element into a dictionary with inferred types."""
    parsed_dict = {}

    if element.text:
        # infer type
        text = element.text.strip()
        if text.isdigit():  # if whole num, treat it as an integer
            parsed_dict[element.tag] = int(text)
        else:
            try:
                parsed_dict[element.tag] = float(text)
            except ValueError:
                if text.lower() == "true":  # treat "true" as a boolean
                    parsed_dict[element.tag] = True
                elif text.lower() == "false":  # treat "false" as a boolean
                    parsed_dict[element.tag] = False
                else:
                    parsed_dict[element.tag] = text

    if len(element):
        child_dict = {}
        for child in element:
            child_parsed = parse_xml_element(child)
            child_dict.update(child_parsed)

        if element.tag in parsed_dict:
            parsed_dict[element.tag].update(child_dict)  # merge with text content if it exists
        else:
            parsed_dict[element.tag] = child_dict

    return parsed_dict