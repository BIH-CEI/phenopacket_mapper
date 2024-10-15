from phenopacket_mapper.utils.io import read_xml
from phenopacket_mapper.utils.io.read_xml import remove_at_symbols

import pytest
from io import StringIO

@pytest.mark.parametrize(
    "inp,expected",
    [
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
    ],
)
# TODO test tags inside tags eg <a b="c">d</a>
def test_read_xml(inp, expected):
    assert read_xml(StringIO(inp)) == expected


@pytest.mark.parametrize(
    "inp,expected",
    [
        ({"@a": "b"}, {"a": "b"}),
        ({"a": "b"}, {"a": "b"}),
        ({'@a': {'@b': 'c'}}, {'a': {'b': 'c'}}),
        ({'a': [{'@b': 'c'}, {'@d': 'e'}]}, {'a': [{'b': 'c'}, {'d': 'e'}]}),
    ]
)
def test_remove_at_symbols(inp, expected):
    assert remove_at_symbols(inp) == expected
