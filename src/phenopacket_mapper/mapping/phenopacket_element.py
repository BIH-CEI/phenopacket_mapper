from dataclasses import dataclass, field
from typing import Any, List

from phenopacket_mapper.mapping import MapElement


@dataclass(frozen=True, slots=True)
class PhenopacketElement:
    phenopacket_element: Any = field()
    fields: List[MapElement] = field()

    def __post_init__(self):
        for f in self.fields:
            if not hasattr(self.phenopacket_element, f.to_field):
                raise AttributeError(f"The class: {self.phenopacket_element} has no attribute {f.to_field}")
            