from dataclasses import dataclass, field
from typing import Union, Tuple

from phenopacket_mapper._api import DataNode
from phenopacket_mapper.data_standards import Cardinality, DataField, DataSection


@dataclass(slots=True, frozen=True)
class OrGroup(DataNode):
    fields: Tuple[Union[DataField, DataSection, 'OrGroup'], ...]
    name: str = field(default='Or Group')
    id: str = field(default=None)
    description: str = field(default='')
    required: bool = field(default=False)
    cardinality: Cardinality = field(default_factory=Cardinality)

    def __post_init__(self):
        if not self.id:
            from phenopacket_mapper.utils import str_to_valid_id
            object.__setattr__(self, 'id', str_to_valid_id(self.name))
