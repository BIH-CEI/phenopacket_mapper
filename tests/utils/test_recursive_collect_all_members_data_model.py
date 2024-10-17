import pytest

from phenopacket_mapper import DataModel
from phenopacket_mapper.data_standards import DataField, DataSection, OrGroup
from phenopacket_mapper.data_standards.data_model import recursive_collect_all_members_data_model

df1 = DataField(
    name="test_field_1",
    specification=str,
)

df2 = DataField(
    name="test_field_2",
    specification=int,
)

df3 = DataField(
    name="test_field_3",
    specification=bool,
)

ds1 = DataSection(
    name="test_section_1",
    fields=(df1, df2)
)

og1 = OrGroup(
    name="test_or_group_1",
    fields=(df1, df2)
)


@pytest.mark.parametrize(
    "data_model, members",
    [
        (
                DataModel(
                    name="test",
                    fields=(df1, df2)
                ),
                [df1, df2]
        ),  # tabular data model

        (
                DataModel(
                    name="test",
                    fields=(ds1, df3)
                ),
                [df1, df2, ds1, df3]
        ),  # hierarchical with section data model

        (
                DataModel(
                    name="test",
                    fields=(og1, df3)
                ),
                [df1, df2, og1, df3]
        ),  # hierarchical with or group data model
    ]
)
def test_recursive_collect_all_members_data_model(data_model, members):
    assert set(recursive_collect_all_members_data_model(data_model)) == set(members)
