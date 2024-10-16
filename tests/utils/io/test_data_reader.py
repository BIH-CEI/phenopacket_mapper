from io import StringIO

import pandas as pd
import pytest
from phenopacket_mapper.utils.io import DataReader


@pytest.mark.parametrize(
    "inp,expected",
    [
        ('<?xml version="1.0" encoding="UTF-8" ?> <ODM xmlns="http://www.cdisc.org/ns/odm/v1.3" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:redcap="https://projectredcap.org" xsi:schemaLocation="http://www.cdisc.org/ns/odm/v1.3 schema/odm/ODM1-3-1.xsd" ODMVersion="1.3.1" FileOID="000-00-0000" FileType="Snapshot" Description="genAdipositas - ALT Demo" AsOfDateTime="2024-10-14T11:57:18" CreationDateTime="2024-10-14T11:57:18" SourceSystem="REDCap" SourceSystemVersion="14.6.9"> '
         '<ClinicalData StudyOID="Project.GenAdipositasALTDemo" MetaDataVersionOID="Metadata.GenAdipositasALTDemo_2024-10-14_1157">'
         '<SubjectData SubjectKey="101" redcap:RecordIdField="record_id">	'
         '</SubjectData>'
         '</ClinicalData>'
         '</ODM>',
         {'ODM': {'AsOfDateTime': '2024-10-14T11:57:18',
                  'ClinicalData': {'MetaDataVersionOID': 'Metadata.GenAdipositasALTDemo_2024-10-14_1157',
                                   'StudyOID': 'Project.GenAdipositasALTDemo',
                                   'SubjectData': {'SubjectKey': 101,
                                                   'redcap:RecordIdField': 'record_id'}},
                  'CreationDateTime': '2024-10-14T11:57:18',
                  'Description': 'genAdipositas - ALT Demo',
                  'FileOID': '000-00-0000',
                  'FileType': 'Snapshot',
                  'ODMVersion': '1.3.1',
                  'SourceSystem': 'REDCap',
                  'SourceSystemVersion': '14.6.9',
                  'xmlns': 'http://www.cdisc.org/ns/odm/v1.3',
                  'xmlns:ds': 'http://www.w3.org/2000/09/xmldsig#',
                  'xmlns:redcap': 'https://projectredcap.org',
                  'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance',
                  'xsi:schemaLocation': 'http://www.cdisc.org/ns/odm/v1.3 '
                                        'schema/odm/ODM1-3-1.xsd'}}
         ),
    ]
)
def test_read_xml(inp, expected):
    data_reader = DataReader(StringIO(inp), file_extension="xml")
    assert data_reader.data == expected


@pytest.mark.parametrize(
    "inp",
    [
        '<a b="b_content" c="c_content">	'
        '</a>',
        '<a b="b_content@@@" c="c_content">'
        '</a>',
    ]
)
def test_read_xml_no_at_symbols_in_keys(inp):
    """
    There are allowed to be at symbols in the data but the post processing function will remove @ symbols that the
    xml to python dictionary reader puts in. Example:
    <a b="b_content" c="c_content"></a>

    will return:
    {'a': {'@b': 'b_content', '@c': 'c_content'}}

    this test exists to ensure that the post processing function is working correctly, returning:
    {'a': {'b': 'b_content', 'c': 'c_content'}}.

    However, to make sure that the postprocessor does not remove @ symbols in the data, there is an additional test case
    """
    data_reader = DataReader(StringIO(inp), file_extension="xml")
    num_at_symbols = str(data_reader.data.keys()).count('@')
    assert num_at_symbols == 0


@pytest.mark.parametrize(
    "inp, expected",
    [
        (
            "a,b,c,d\n1,1.23,False,hello\n2,-123,FALSE,how\n3,.5,TRUE,#!$%$^@&*/\n4,0.5,True,are\n5,0,true,you",
            pd.DataFrame(
                {
                    "a": [1, 2, 3, 4, 5],
                    "b": [1.23, -123, 0.5, 0.5, 0],
                    "c": [False, False, True, True, True],
                    "d": ["hello", "how", "#!$%$^@&*/", "are", "you"],
                }
            )
        )
    ]
)
def test_reader_csv(inp, expected):
    data_reader = DataReader(StringIO(inp), file_extension="csv")
    assert set(data_reader.data.columns) == set(expected.columns)
    for col in expected.columns:
        assert data_reader.data[col].equals(expected[col])


@pytest.mark.parametrize(
    "inp,expected",
    [
        ('{"string": "Hello World"}', {"string": "Hello World"}),
        ('{"object": {"a": "b","c": "d"}}', {"object": {"a": "b","c": "d"}}),
        ('{"number": 123}', {"number": 123}),
        ('{"number": -123}', {"number": -123}),
        ('{"number": 123.4}', {"number": 123.4}),
        ('{"null": null}', {"null": None}),
        ('{"color": "gold"}', {"color": "gold"}),
        ('{"boolean": true}', {"boolean": True}),
        ('{"boolean": false}', {"boolean": False}),
        ('{"array": [1,2,3]}', {"array": [1,2,3]}),
        ('{"array": [1,2,3],"boolean": true, "color": "gold","null": null,"number": 123, "object": {"a": "b","c": "d"}, "string": "Hello World"}', {"array": [1,2,3],"boolean": True, "color": "gold","null": None, "number": 123, "object": {"a": "b","c": "d"}, "string": "Hello World"})
    ],
)
def test_reader_json(inp, expected):
    data_reader = DataReader(StringIO(inp), file_extension="json")
    assert data_reader.data == expected