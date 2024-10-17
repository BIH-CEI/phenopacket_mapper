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

    def __str__(self):
        return f"{self.min}..{self.max}"

    # Singleton instances
    _instances = {}

    @classmethod
    @property
    def ZERO_TO_ONE(cls) -> 'Cardinality':
        if 'ZERO_TO_ONE' not in cls._instances:
            cls._instances['ZERO_TO_ONE'] = cls(0, 1)
        return cls._instances['ZERO_TO_ONE']

    @classmethod
    @property
    def ZERO_TO_N(cls) -> 'Cardinality':
        if 'ZERO_TO_N' not in cls._instances:
            cls._instances['ZERO_TO_N'] = cls(0, 'n')
        return cls._instances['ZERO_TO_N']

    @classmethod
    @property
    def ONE(cls) -> 'Cardinality':
        if 'OPTIONAL' not in cls._instances:
            cls._instances['ONE'] = cls(1, 1)
        return cls._instances['ONE']

    @classmethod
    @property
    def ONE_TO_N(cls) -> 'Cardinality':
        if 'ONE_TO_N' not in cls._instances:
            cls._instances['ONE_TO_N'] = cls(1, 'n')
        return cls._instances['ONE_TO_N']

