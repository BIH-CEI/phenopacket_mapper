"""
This package is intended to expose the PhenopacketMapper API to the user.
"""

from abc import ABCMeta, abstractmethod, abstractproperty
from typing import Tuple, Iterable, Iterator
from dataclasses import dataclass


class DataModelDefiner(metaclass=ABCMeta):
    """
    Take some data model definition and try to load it into :class:`DataModel`.

    E.g. protobuf model "definer".
    """
    pass


class DataModel(metaclass=ABCMeta):
    """
    Value class.
    The fields:
     - label, version
     - a root `DataNode`, it must be there (not `Optional`)
     - resources (maybe generate dynamically, or keep as a list)

    We want to be able to (de)serialize this.
    """
    pass


class DataNode(metaclass=ABCMeta):
    """
    This is very much like Jackson (Java) `TreeNode`,
    because it can be many things.

    The common things may include
    - label
    - maybe it knows about the parent (optional) and children

    We want to be able to (de)serialize this.
    """
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def required(self) -> bool:
        pass


    @property
    @abstractmethod
    def description(self) -> str:
        pass


class DataInstance:
    pass


class Transformation(metaclass=ABCMeta):
    """

    """
    steps: Tuple


class Mapper:

    def __init__(
        self,
        transformation: Transformation,
    ):
        pass

    def transform_dataset(
        self,
        data_set: Iterable[DataInstance],
    ) -> Iterator[DataInstance]:
        return map(lambda item: self.transform(item), data_set)

    def transform(self, item: DataInstance) -> DataInstance:
        # TODO: implement based on self.transformation
        pass
