from typing import List, Literal, Union

from phenopacket_mapper.data_standards import CodeSystem, Coding, CodeableConcept, Date
from phenopacket_mapper.utils.parsing import parse_primitive_data_value, parse_date, parse_coding


def parse_value(
        value_str: str,
        resources: List[CodeSystem],
        compliance: Literal['strict', 'lenient'] = 'lenient'
) -> Union[Coding, CodeableConcept, CodeSystem, str, bool, int, float, Date, type]:
    """Parses a string representing a value to the appropriate type
    
    This method acts as a wrapper for the parsing of different types of values. It tries to parse the value from
    different types in the following order:
    1. Primitive data value (`parse_primitive_data_value`)
    2. Date (`parse_date`)
    3. Coding (`parse_coding`)
    4. String (if nothing else worked)

    :param value_str: String representation of the value
    :param resources: List of CodeSystems to use for parsing the value
    :param compliance: Compliance level for parsing the value
    :return: The parsed value
    """
    value_str = value_str.strip()

    # parsing as a date
    try:
        value = parse_date(date_str=value_str, compliance='strict')
    except ValueError:
        pass
    else:
        return value

    # parsing as a coding
    try:
        value = parse_coding(coding_str=value_str, resources=resources, compliance='strict')
    except ValueError:
        pass
    else:
        return value

    # parsing as a primitive value
    # has to be tried last, otherwise it defaults to parsing as a string
    try:
        value = parse_primitive_data_value(value_str=value_str)
    except ValueError:
        pass
    else:
        return value

    if compliance == 'strict':
        raise ValueError(f"Could not parse value: {value_str}")
    else:
        print(f"Warning: Could not parse value: {value_str}")
        return value_str
