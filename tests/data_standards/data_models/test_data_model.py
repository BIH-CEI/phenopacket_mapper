import pytest

from phenopacket_mapper.data_standards import DataModel, DataField
from phenopacket_mapper.data_standards.value_set import ValueSet


@pytest.fixture
def data_model():
    return DataModel(resources=[], data_model_name='test_data_model', fields=[
        DataField(name='Field 0', value_set=ValueSet()),
        DataField(name='Date of Birth', value_set=ValueSet()),
        DataField(name='%^&#12pseudonym!2', value_set=ValueSet()),
    ])


def test_get_data_field_by_id(data_model):
    assert data_model.field_0.name == 'Field 0'
    assert data_model.date_of_birth.name == 'Date of Birth'
    assert data_model._12pseudonym_2.name == '%^&#12pseudonym!2'
