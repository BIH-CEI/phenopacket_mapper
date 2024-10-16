from io import StringIO

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