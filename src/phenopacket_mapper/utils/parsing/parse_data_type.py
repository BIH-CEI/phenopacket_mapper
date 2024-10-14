from typing import List, Union, Any, Literal

from phenopacket_mapper.data_standards import CodeSystem, Date
from phenopacket_mapper.utils.parsing import get_codesystem_by_namespace_prefx

PRIMITIVE_DATATYPE_SYNONYMS = {
    str: ["str", "string"],
    int: ["int", "integer"],
    float: ["float", "double"],
    bool: ["boolean", "bool"],
    Date: ["date", "yyyy-mm-dd", "yyyy/mm/dd", "mm/dd/yyyy", "mm-dd-yyyy", "dd/mm/yyyy", "dd.mm.yyyy", "dd-mm-yyyy",
           "yyyy-mm", "yyyy/mm", "yyyy.mm", "mm.yyyy", "mm-yyyy", "mm/yyyy", "yyyy", "yyyy-mm-dd hh:mm:ss", "iso8601"]
}


def parse_data_type(
        type_str: str,
        resources: List[CodeSystem],
        compliance: Literal['lenient', 'strict'] = 'lenient'
) -> List[Union[Any, CodeSystem, type, str]]:
    """Parses a string representing of one or multiple data types or code systems to a list of `type` in Python

    The purpose of this method is to parse entries in a Data Model tabular file for `DataField.data_type`. In the
    tabular file, the user can list typical primitive data types such as string, int, etc., or date as a data type.
    Further is it possible to list the name space prefix (e.g., "SCT" for SNOMED CT) of a specific resource (given its
    inclusion in the list passed as the `resources` parameter) to indicate that codes or terms from that resource are
    permittable.

    When `compliance` is set to `'lenient'` (default), this method only issues warnings if a data type is unrecognized and
    adds a literal to the list of allowed data types. When `compliance` is set to `'strict'`, it throws a `ValueError` in
    the case described above.

    E.g.
    >>> parse_data_type("integer, str, Boolean", [])
    [<class 'int'>, <class 'str'>, <class 'bool'>]

    :param type_str:
    :param resources:
    :param compliance:
    :return:
    """
    if not type_str or not type_str.strip():  # checks for all sorts of empty strings, with however many white spaces
        return [Any]

    single_type_strings = type_str.split(',')
    types = []
    for single in single_type_strings:
        types.append(parse_single_data_type(type_str=single, resources=resources, compliance=compliance))

    if not types:
        return [Any]

    return types


def parse_single_data_type(
        type_str: str,
        resources: List[CodeSystem],
        compliance: Literal['lenient', 'strict'] = 'lenient'
) -> Union[Any, CodeSystem, type, str]:
    """Parses a string representing a data type to the `type` in Python

    E.g.:
    >>> parse_single_data_type('date', [])
    <class 'phenopacket_mapper.data_standards.date.Date'>

    :param type_str:
    :param resources:
    :param compliance:
    :return:
    """
    type_str = type_str.strip()

    code_system = get_codesystem_by_namespace_prefx(namespace_prefix_str=type_str, resources=resources)

    if code_system:
        return code_system

    for type_ in PRIMITIVE_DATATYPE_SYNONYMS.keys():
        for syn in PRIMITIVE_DATATYPE_SYNONYMS[type_]:
            if syn.lower() == type_str.lower():
                return type_

    # if nothing has matched
    if compliance == 'lenient':
        print(f"Warning: The type {type_str} could not be parsed to a type or resource. If it refers to a resource,"
              f" please add it to the list of resources. Otherwise, check your file.")
        return type_str
    else:
        raise ValueError(f"No matching data types or resources could be found for '{type_str}'")
