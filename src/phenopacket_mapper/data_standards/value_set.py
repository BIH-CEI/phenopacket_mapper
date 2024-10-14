import warnings
from dataclasses import dataclass, field
from typing import List, Union, Literal

from phenopacket_mapper.data_standards import Coding, CodeableConcept, CodeSystem, Date


@dataclass(slots=True, frozen=True)
class ValueSet:
    """Defines a set of values that can be used in a DataField

    A value set defines the viable values for a DataField. It can be a list of values, codings, codeable concepts,
    dates, etc. Also, it can just list types or CodeSystems that are allowed for a DataField.

    Example usecases:
    - True, False, or Unknown
    - only allow strings
    - allow any numerical value (i.e., int, float)
    - allow any date
    - allow any code from one or more CodeSystems
    - allow only a specific set of codings
    - etc.

    By assigning a ValueSet to a DataField, we can define the possible values for that field. This has multiple benefits
    : it allows for validation of the data, it facilitates the computability of the data, and it allows for
    better interoperability between different systems.

    :ivar elements: List of elements that define the value set
    :ivar name: Name of the value set
    :ivar description: Description of the value set
    """
    elements: List[Union[Coding, CodeableConcept, CodeSystem, str, bool, int, float, Date, type]] \
        = field(default_factory=list)
    name: str = field(default="")
    description: str = field(default="")
    _resources: List[CodeSystem] = field(default_factory=list, repr=False)

    def __post_init__(self):
        if Coding in self.elements or CodeableConcept in self.elements:
            warnings.warn("The ValueSet contains Coding or CodeableConcept. It is recommended to limit the dataset to"
                          "the CodeSystems that are used in the DataField. This will improve the interoperability of"
                          "the data. E.g., try adding the SNOMED-CT CodeSystem to the ValueSet.")

    def extend(self, new_name: str, value_set: 'ValueSet', new_description: str = '') -> 'ValueSet':
        return ValueSet(name=new_name,
                        elements=list(set(self.elements + value_set.elements)),
                        description=new_description)

    def remove_duplicates(self) -> 'ValueSet':
        return ValueSet(name=self.name,
                        elements=list(set(self.elements)),
                        description=self.description)

    @property
    def resources(self) -> List[CodeSystem]:
        """Returns the resources if they exist, otherwise provides a default empty list."""
        if len(self._resources) == 0:
            for e in self.elements:
                if isinstance(e, CodeSystem):
                    self._resources.append(e)
        return self._resources

    @staticmethod
    def parse_value_set(
            value_set_str: str,
            value_set_name: str = "",
            value_set_description: str = "",
            resources: List[CodeSystem] = None,
            compliance: Literal['strict', 'lenient'] = 'lenient',
    ) -> 'ValueSet':
        """Parses a value set from a string representation

        >>> ValueSet.parse_value_set("True, False", "TrueFalseValueSet", "A value set for True and False", [])
        ValueSet(elements=[True, False], name='TrueFalseValueSet', description='A value set for True and False')

        >>> ValueSet.parse_value_set("-1, 0, 1", resources=[])
        ValueSet(elements=[-1, 0, 1], name='', description='')

        :param value_set_str: String representation of the value set
        :param value_set_name: Name of the value set
        :param value_set_description: Description of the value set
        :param resources: List of CodeSystems to use for parsing the value set
        :param compliance: Compliance level for parsing the value set
        :return: A ValueSet object as defined by the string representation
        """
        from phenopacket_mapper.utils.parsing.parse_value_set import parse_value_set
        return parse_value_set(
            value_set_str=value_set_str,
            value_set_name=value_set_name,
            value_set_description=value_set_description,
            resources=resources,
            compliance=compliance,
        )

    def __contains__(self, item):
        from phenopacket_mapper.data_standards import DataFieldValue
        if isinstance(item, bool):
            for element in self.elements:
                if isinstance(element, bool) and element == item:
                    return True
        elif type(item) in [Coding, CodeableConcept, CodeSystem, str, int, float, Date, type]:
            for element in self.elements:
                if element == item:
                    return True
        elif isinstance(item, DataFieldValue):
            for element in self.elements:
                if element == item.value:
                    return True
        return False

    def __iter__(self):
        yield from self.elements


TRUE_FALSE_VALUE_SET = ValueSet(name="TrueFalseValueSet",
                                elements=[True, False],
                                description="A value set for True and False")

UNKNOWN_VALUE_SET = ValueSet(name="UnknownValueSet",
                             elements=["unknown"],
                             description="A value set for Unknown")

TRUE_FALSE_UNKNOWN_VALUE_SET = TRUE_FALSE_VALUE_SET.extend(new_name="TrueFalseUnknownValueSet",
                                                           value_set=UNKNOWN_VALUE_SET,
                                                           new_description="A value set for True, False, and Unknown")
