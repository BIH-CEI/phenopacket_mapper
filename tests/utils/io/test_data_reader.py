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
        ('<string>Hello World</string>', {"string": "Hello World"}),
        ('<object><a>b</a><c>d</c></object>', {"object": {"a": "b", "c": "d"}}),
        ('<number>123</number>', {"number": 123}),
        ('<number>-123</number>', {"number": -123}),
        ('<number>123.4</number>', {"number": 123.4}),
        ('<null></null>', {"null": None}),  # empty tag
        ('<null />', {"null": None}),  # empty tag
        ('<null xsi:nil="true"/>', {"null": None}),  # explicit null
        ('<color>gold</color>', {"color": "gold"}),
        ('<boolean>true</boolean>', {"boolean": True}),
        ('<boolean>false</boolean>', {"boolean": False}),
        ('<array><item>1</item><item>2</item><item>3</item></array>', {"array": {"item": [1, 2, 3]}}),
        ('<root>'
         '<array>'
         '<item>1</item>'
         '<item>2</item>'
         '<item>3</item>'
         '</array>'
         '<boolean>true</boolean>'
         '<color>gold</color>'
         '<number>123</number>'
         '<object>'
         '<a>b</a>'
         '<c>d</c>'
         '</object>'
         '<string>Hello World</string>'
         '</root>',
         {
             "root":{
                 "array": {
                     "item": [1, 2, 3]
                 },
                 "boolean": True,
                 "color": "gold",
                 "number": 123,
                 "object": {
                     "a": "b",
                     "c": "d"
                 },
                 "string": "Hello World"
             }
         }),
        ('<ItemData ItemOID="redcap_survey_identifier" Value=""/>', {"ItemData": {"ItemOID": "redcap_survey_identifier", "Value": ""}}),

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


@pytest.mark.parametrize(
    "inp, expected, file_extension",
    [
        (
            [
                '{"pat_id": "patient_426387", "name":"Joe Johnson", "condition": {"term_id": "1253", "term_label": "acute_madeupgitis"}, "hospitalized": true}',
                '{"pat_id": "patient_426388", "name":"Jane Doe", "condition": {"term_id": "1254", "term_label": "chronic_madeupgitis"}, "hospitalized": false}',
                '{"pat_id": "patient_426389", "name":"Mark Markington", "condition": {"term_id": "1255", "term_label": "wild_type_madeupgitis"}, "hospitalized": true}'
            ],
            [
                {'pat_id': 'patient_426387', 'name':'Joe Johnson', 'condition': {'term_id': '1253', 'term_label': 'acute_madeupgitis'}, 'hospitalized': True},
                {'pat_id': 'patient_426388', 'name':'Jane Doe', 'condition': {'term_id': '1254', 'term_label': 'chronic_madeupgitis'}, 'hospitalized': False},
                {'pat_id': 'patient_426389', 'name':'Mark Markington', 'condition': {'term_id': '1255', 'term_label': 'wild_type_madeupgitis'}, 'hospitalized': True}
            ],
            'json'
        ),
        (
            [
                '<?xml version="1.0" encoding="UTF-8" ?> '
                '<ODM>'
                '<ClinicalData StudyOID="test_study" MetaDataVersionOID="Metadata.test_study_2024-10-16_1142">'
                '<SubjectData SubjectKey="101" redcap:RecordIdField="record_id">'
                '<Item id="patient_name">Joe Johnson</Item>'
                '<Section id="condition">'
                '<Item id="term_id">12353</Item>'
                '<Item id="term_label">acute_madeupgitis</Item>'
                '</Section>'
                '<Item id="hospitalized">true</Item>'
                '</SubjectData>'
                '</ClinicalData>'
                '</ODM>',

                '<?xml version="1.0" encoding="UTF-8" ?> '
                '<ODM>'
                '<ClinicalData StudyOID="test_study" MetaDataVersionOID="Metadata.test_study_2024-10-16_1142">'
                '<SubjectData SubjectKey="102" redcap:RecordIdField="record_id">'
                '<Item id="patient_name">Jane Doe</Item>'
                '<Section id="condition">'
                '<Item id="term_id">12354</Item>'
                '<Item id="term_label">chronic_madeupgitis</Item>'
                '</Section>'
                '<Item id="hospitalized">false</Item>'
                '</SubjectData>'
                '</ClinicalData>'
                '</ODM>',

                '<?xml version="1.0" encoding="UTF-8" ?> '
                '<ODM>'
                '<ClinicalData StudyOID="test_study" MetaDataVersionOID="Metadata.test_study_2024-10-16_1142">'
                '<SubjectData SubjectKey="103" redcap:RecordIdField="record_id">'
                '<Item id="patient_name">Mark Markington</Item>'
                '<Section id="condition">'
                '<Item id="term_id">12355</Item>'
                '<Item id="term_label">wild_type_madeupgitis</Item>'
                '</Section>'
                '<Item id="hospitalized">true</Item>'
                '</SubjectData>'
                '</ClinicalData>'
                '</ODM>',
            ],
            [
                {'ODM': {'ClinicalData': {'MetaDataVersionOID': 'Metadata.test_study_2024-10-16_1142',
                                          'StudyOID': 'test_study',
                                          'SubjectData': {'Item': [{'#text': 'Joe Johnson',
                                                                    'id': 'patient_name'},
                                                                   {'#text': True,
                                                                    'id': 'hospitalized'}],
                                                          'Section': {'Item': [{'#text': 12353,
                                                                                'id': 'term_id'},
                                                                               {'#text': 'acute_madeupgitis',
                                                                                'id': 'term_label'}],
                                                                      'id': 'condition'},
                                                          'SubjectKey': 101,
                                                          'redcap:RecordIdField': 'record_id'}}}},
                {'ODM': {'ClinicalData': {'MetaDataVersionOID': 'Metadata.test_study_2024-10-16_1142',
                                          'StudyOID': 'test_study',
                                          'SubjectData': {'Item': [{'#text': 'Jane Doe',
                                                                    'id': 'patient_name'},
                                                                   {'#text': False,
                                                                    'id': 'hospitalized'}],
                                                          'Section': {'Item': [{'#text': 12354,
                                                                                'id': 'term_id'},
                                                                               {'#text': 'chronic_madeupgitis',
                                                                                'id': 'term_label'}],
                                                                      'id': 'condition'},
                                                          'SubjectKey': 102,
                                                          'redcap:RecordIdField': 'record_id'}}}},
                {'ODM': {'ClinicalData': {'MetaDataVersionOID': 'Metadata.test_study_2024-10-16_1142',
                                          'StudyOID': 'test_study',
                                          'SubjectData': {'Item': [{'#text': 'Mark Markington',
                                                                    'id': 'patient_name'},
                                                                   {'#text': True,
                                                                    'id': 'hospitalized'}],
                                                          'Section': {'Item': [{'#text': 12355,
                                                                                'id': 'term_id'},
                                                                               {'#text': 'wild_type_madeupgitis',
                                                                                'id': 'term_label'}],
                                                                      'id': 'condition'},
                                                          'SubjectKey': 103,
                                                          'redcap:RecordIdField': 'record_id'}}}}
            ],
            'xml'
        ),
    ]
)
def test_reader_list(inp, expected, file_extension):
    for fe in [file_extension, file_extension.lower(), file_extension.upper()]:
        buffers = [StringIO(f) for f in inp]
        data = DataReader(buffers, file_extension=fe).data
        for d, e in zip(data, expected):
            assert d == e