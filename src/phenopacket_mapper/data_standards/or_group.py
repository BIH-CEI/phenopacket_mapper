from dataclasses import dataclass, field
from typing import Union, Tuple

from phenopacket_mapper.data_standards import DataField, DataSection


@dataclass(slots=True, frozen=True)
class OrGroup:
    fields: Tuple[Union[DataField, DataSection], ...]