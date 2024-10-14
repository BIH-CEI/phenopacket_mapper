from typing import List, Literal, Any

from phenopacket_mapper.data_standards import CodeSystem
from phenopacket_mapper.utils.parsing import parse_single_data_type, parse_value
from phenopacket_mapper.data_standards.value_set import ValueSet


def parse_value_set(
        value_set_str: str,
        value_set_name: str = "",
        value_set_description: str = "",
        resources: List[CodeSystem] = None,
        compliance: Literal['strict', 'lenient'] = 'lenient',
) -> ValueSet:
    """Parses a value set from a string representation

    >>> ValueSet.parse_value_set("True, False", resources=[])
    ValueSet(elements=[True, False], name='', description='')

    :param value_set_str: String representation of the value set
    :param value_set_name: Name of the value set
    :param value_set_description: Description of the value set
    :param resources: List of CodeSystems to use for parsing the value set
    :param compliance: Compliance level for parsing the value set
    :return: A ValueSet object as defined by the string representation
    """
    if not isinstance(value_set_str, str) or not value_set_str:
        if compliance == 'strict':
            raise ValueError(f"value_set_str must be a string, not {type(value_set_str)} ({value_set_str})")
        else:
            return ValueSet(elements=[Any], description=value_set_description)

    value_set_str = value_set_str.strip()

    if resources is None:
        resources = []

    elements_str = value_set_str.split(",")

    elements = []
    for element_str in elements_str:
        element_str = element_str.strip()

        # parsing as a data type
        try:
            # compliance is set to 'strict' because we want to raise an error if the element is not recognized
            element = parse_single_data_type(type_str=element_str, resources=resources, compliance='strict')
        except ValueError:  # parsing as type failed, parsing as a value
            element = parse_value(value_str=element_str, resources=resources)

        if element is not None:
            elements.append(element)
        else:
            if compliance == 'strict':
                raise ValueError(f"Could not parse element: {element_str}")
            else:
                elements.append(element_str)

    return ValueSet(name=value_set_name, elements=elements, description=value_set_description)
