from dataclasses import dataclass, field
from typing import Union, Literal


@dataclass(slots=True, frozen=True)
class Cardinality:
    min: int = field(default=0)
    max: Union[int, Literal['n']] = field(default='n')