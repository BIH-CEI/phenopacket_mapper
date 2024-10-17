from typing import Any

import pytest

from phenopacket_mapper.data_standards import Date
from phenopacket_mapper.data_standards.code_system import HPO, SNOMED_CT, ICD10CM, ICD9
from phenopacket_mapper.utils.parsing.parse_data_type import \
    parse_single_data_type, parse_data_type


@pytest.fixture
def resources():
    return [
        HPO,
        SNOMED_CT,
        ICD10CM,
        ICD9
    ]

@pytest.mark.parametrize(
    "type_str, result", [
        ("str", [str]),  # single primitive
        ("integer", [int]),  # single primitive
        ("integer, bool", [int, bool]),  # 2 primitive, white space
        ("integer,bool", [int, bool]),  # 2 primitive, no white space
        (" integer ,   bool ", [int, bool]),  # 2 primitive, multiple white spaces
        ("integer,bool, string", [int, bool, str]),  # multiple primitives space and no soace
        ("integer, bool, string", [int, bool, str]),  # multiple primitives
        ("Int, bOoL, StRInG", [int, bool, str]),  # multiple primitives spongebob case
        ("INT, BOOLEAN, STR", [int, bool, str]),  # multiple primitives upper case
        ("", [Any]),  # empty string
        (" ", [Any]),  # empty string
        ("               ", [Any]),  # empty string
        (None, [Any]), # empty string
        ("icd9", [ICD9]), # single resource
        ("icd10cm", [ICD10CM]),  # single resource
        ("icd10cm, hpo", [ICD10CM, HPO]),  # multiple resources
        ("hpo, sct, str", [HPO, SNOMED_CT, str]),  # mix resources and primitives
        ("hPo, SNOmed, strinG", [HPO, SNOMED_CT, str]),  # mix resources and primitives, strange upper and lower
        ("date", [Date]),
        ("date, snomed, hpo", [Date, SNOMED_CT, HPO]),
        ("integer, boolean, string, date, HP", [int, bool, str, Date, HPO]),
    ]
)
def test_parse_data_type(type_str, result, resources):
    assert parse_data_type(type_str, resources) == result


@pytest.mark.parametrize(
    "type_str, result", [
        ("str", str),  # single primitive
        ("integer", int),  # single primitive
        ("integer ", int),  # white space
        (" integer   ", int),  # multiple white spaces
        ("Int", int),  # spongebob case
        ("bOoL", bool),  # spongebob case
        ("StRInG", str),  # spongebob case
        ("INT", int),  # primitive upper case
        ("BOOLEAN", bool),  # primitive upper case
        ("STR", str),  # primitive upper case
        # no need to check for empty strings because this is a helper and the bigger method checks and is tested
        ("icd9", ICD9),  #single resource
        ("icd10-cm", ICD10CM),  # single resource
        ("hpo", HPO),  # single resources
        ("icd10_cm", ICD10CM),  # synonym
        ("icd-9", ICD9),  # synonym
    ]
)
def test__parse_single_data_type(type_str, result, resources):
    assert parse_single_data_type(type_str, resources) == result


@pytest.mark.parametrize("type_str, result", [
    ("date", Date),
    ("Date", Date),
    # all formattings that Date.formatted_string can handle
    ("yyyy-mm-dd", Date),
    ("yyyy/mm/dd", Date),
    ("mm/dd/yyyy", Date),
    ("mm-dd-yyyy", Date),
    ("dd/mm/yyyy", Date),
    ("dd.mm.yyyy", Date),
    ("dd-mm-yyyy", Date),
    ("yyyy-mm", Date),
    ("yyyy/mm", Date),
    ("yyyy.mm", Date),
    ("mm.yyyy", Date),
    ("mm-yyyy", Date),
    ("mm/yyyy", Date),
    ("yyyy", Date),
    ("yyyy-mm-dd hh:mm:ss", Date),
    ("iso8601", Date),
])
def test_parse_data_type_date(type_str, result):
    assert parse_single_data_type(type_str, []) == result
    assert parse_data_type(type_str, []) == [result]
