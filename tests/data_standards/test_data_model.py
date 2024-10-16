import pytest
from phenopacket_mapper import DataModel

from phenopacket_mapper.data_standards import DataField

class TestDataModel:

    @staticmethod
    @pytest.mark.parametrize(
        "inp, expected",
        [
            (
                DataModel(
                    data_model_name="test",
                    fields=(
                        DataField(
                            name="test_field",
                            specification=int
                        ),
                        DataField(
                            name="test_field2",
                            specification=str
                        ),
                    )
                ),
                False
            ),
        ]
    )
    def test_data_model(inp: DataModel, expected):
        assert inp.is_hierarchical == expected