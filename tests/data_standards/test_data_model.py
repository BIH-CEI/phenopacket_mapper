import pytest

from phenopacket_mapper.data_standards import DataModel, DataField, DataSection, OrGroup
from phenopacket_mapper.data_standards.value_set import ValueSet


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

    @staticmethod
    @pytest.fixture
    def data_model():
        return DataModel(resources=tuple(), data_model_name='test_data_model', fields=(
            DataField(name='Field 0', specification=ValueSet()),
            DataField(name='Date of Birth', specification=ValueSet()),
            DataField(name='%^&#12pseudonym!2', specification=ValueSet()),
        ))


    @staticmethod
    def test_get_data_field_by_id(data_model):
        assert data_model.field_0.name == 'Field 0'
        assert data_model.get_field('field_0').name == 'Field 0'
        assert data_model.date_of_birth.name == 'Date of Birth'
        assert data_model.get_field('date_of_birth').name == 'Date of Birth'
        assert data_model._12pseudonym_2.name == '%^&#12pseudonym!2'
        assert data_model.get_field('_12pseudonym_2').name == '%^&#12pseudonym!2'
