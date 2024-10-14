import pytest

from phenopacket_mapper.data_standards import Cardinality


@pytest.mark.parametrize(
    "inp, expected", [
        ((0, 1), Cardinality(0, 1)),
        ((1, 1), Cardinality(1, 1)),
        ((0, 'n'), Cardinality(0, 'n')),
        ((1, 'n'), Cardinality(1, 'n')),
        ((0, 3), Cardinality(0, 3)),
    ]
)
def test_cardinality_instantiation(inp, expected):
    assert Cardinality(*inp) == expected


@pytest.mark.parametrize(
    "inp, exc_", [
        ((-1, 1), ValueError),
        ((-1, -1), ValueError),
        ((1, -1), ValueError),
        ((0, 0), ValueError),
        ((0, 'm'), ValueError),
        ((1.0, 'n'), ValueError),
        ((1.3, 'n'), ValueError),
    ]
)
def test_cardinality_instantiation_raises(inp, exc_):
    with pytest.raises(exc_):
        Cardinality(*inp)