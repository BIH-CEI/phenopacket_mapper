from phenopacket_mapper.utils.io import read_xml

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
        ('<null/>', {"null": None}),
        ('<color>gold</color>', {"color": "gold"}),
        ('<boolean>true</boolean>', {"boolean": True}),
        ('<boolean>false</boolean>', {"boolean": False}),
        ('<array><item>1</item><item>2</item><item>3</item></array>', {"array": [1, 2, 3]}),
        ('<root>'
         '<array><item>1</item><item>2</item><item>3</item></array>'
         '<boolean>true</boolean>'
         '<color>gold</color>'
         '<null/>'
         '<number>123</number>'
         '<object><a>b</a><c>d</c></object>'
         '<string>Hello World</string>'
         '</root>',
         {"root":{"array": [1, 2, 3], "boolean": True, "color": "gold", "null": None, "number": 123, "object": {"a": "b", "c": "d"}, "string": "Hello World"}}
         )
    ],
)
def test_read_xml(inp, expected):
    assert read_xml(StringIO(inp)) == expected
