"""This submodule defines the data standards used in the project."""
from typing import Union

from .cardinality import Cardinality
from .or_group import OrGroup
from .date import Date
from .code_system import CodeSystem, SNOMED_CT, HPO, MONDO, OMIM, ORDO, LOINC
from .code import Coding, CodeableConcept
from .data_model import DataModel, DataField, DataModelInstance, DataFieldValue, DataSet, DataSection
from . import data_models
from .value_set import ValueSet

data_node_classes = Union[DataField, DataSection, OrGroup]

__all__ = [
    "Cardinality",
    "OrGroup",
    "Coding", "CodeableConcept",
    "DataModel", "DataField", "DataModelInstance", "DataFieldValue", "DataSet", "DataSection",
    "data_models",
    "CodeSystem",
    "SNOMED_CT", "HPO", "MONDO", "OMIM", "ORDO", "LOINC",
    "Date",
    "ValueSet",
    "data_node_classes",
]
