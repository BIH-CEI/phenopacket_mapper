from dataclasses import dataclass, field
from typing import Union, Literal


@dataclass(slots=True, frozen=True)
class Cardinality:
    min: int = field(default=0)
    max: Union[int, Literal['n']] = field(default='n')

    def __post_init__(self):
        if not isinstance(self.min, int):
            raise ValueError(f"Parameter min must be of type integer. (Not: {type(self.min)})")
        elif self.min < 0:
            raise ValueError(f"Parameter min must be a non-negative integer. (Not: {self.min})")
        if not (isinstance(self.max, int) or self.max == 'n'):
            raise ValueError(f"Parameter max must be of type or equal to the literal 'n'. "
                             f"(Not: {self.min} ({type(self.min)}))")
        elif self.max != 'n' and self.max < 1:  # has to be an integer
            raise ValueError(f"Parameter max must be a positive integer. (Not: {self.min})")