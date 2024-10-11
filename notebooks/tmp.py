from typing import List

from phenopacket_mapper._api import Transformation
from phenopacket_mapper.data_standards import DataModel, DataField

dm1 = DataModel(
    data_model_name="Example data model",
    fields=(
        DataField("pseudonym", str),

    ),
    resources=[]
)

phenopacket_schema = DataModel(
    data_model_name="PP Schema",
    fields=(
        DataField("id", str),
        DataSection("phenotypic_features", List[str]),
        DataSection(
            "subject",
            fields=(
                DataField("id", str),
                DataField("date_of_birth", str),
                DataSection(
            )
        ),
    ),
    resources=[]
)

data = dm1.load_data(
    path="data.csv",
    pseudonym_column="1.1. Pseudonym"
)

t = Transformation(
    source=dm1,
    target=phenopacket_schema,
    id=dm1.pseudonym,
)

# steps

mapper = Mapper(t)

mapped_datae = mapper.map(data)

"""
Warning: phenopacket schema id expects an str, not a int, 
"""

mapped =

