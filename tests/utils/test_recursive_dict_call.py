import pytest


@pytest.mark.parametrize(
    "dict_, keys_list, expected",
    [
        ({'a': 1, 'b': 2}, ['a'], 1),
    ]
)
def test_recursive_dict_call(dict_, keys_list, expected):
    from phenopacket_mapper.utils import recursive_dict_call
    assert recursive_dict_call(dict_, keys_list) == expected
