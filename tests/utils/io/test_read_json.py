from io import StringIO

import pytest

from phenopacket_mapper.utils.io import read_json


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
def test_read_json(inp, expected):
    assert read_json(StringIO(inp)) == expected