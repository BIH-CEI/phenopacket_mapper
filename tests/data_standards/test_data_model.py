import pytest
from phenopacket_mapper import DataModel

from phenopacket_mapper.data_standards import DataField, DataSection, OrGroup


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
                            DataSection(
                                name="test_data_section",
                                fields=(
                                    DataField(
                                        name="test_field3",
                                        specification=bool
                                    ),
                                )
                            )
                        )
                    ),
                    True
            ),
            (
                DataModel(
                    data_model_name="test",
                        fields=(
                            DataField(
                                name="test_field",
                                specification=int
                            ),
                            OrGroup(
                                name="test_or_group",
                                fields=(
                                    DataField(
                                        name="test_field2",
                                        specification=str
                                    ),
                                    DataSection(
                                        name="test_data_section",
                                        fields=(
                                                DataField(
                                                    name="test_field3",
                                                    specification=bool
                                                ),
                                        )
                                    )
                                )
                            ),
                        )
                    ),
                    True
            ),
        ]
    )
    def test_data_model(inp: DataModel, expected):
        assert inp.is_hierarchical == expected