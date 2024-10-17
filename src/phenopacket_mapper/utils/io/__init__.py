"""This module handles the input and output of data."""

from .read_json import read_json
from .read_xml import read_xml, parse_xml
from .data_reader import DataReader
from .input import read_data_model, read_phenopackets, read_phenopacket_from_json, load_tabular_data_using_data_model
from .input import load_hierarchical_data, load_hierarchical_dataset
from .output import write

__all__ = [
    'read_json',
    'read_xml', 'parse_xml',
    'DataReader',
    'read_data_model',
    'read_phenopackets',
    'read_phenopacket_from_json',
    'load_tabular_data_using_data_model',
    'load_hierarchical_data', 'load_hierarchical_dataset',
    'write',
]
