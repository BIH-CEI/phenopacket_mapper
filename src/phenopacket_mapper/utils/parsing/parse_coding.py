from typing import Literal, List
import re

from phenopacket_mapper.data_standards import Coding, CodeSystem
from phenopacket_mapper.utils.parsing import get_codesystem_by_namespace_prefx
from phenopacket_mapper.data_standards import code_system as code_system_module


def parse_coding(
        coding_str: str,
        resources: List[CodeSystem],
        compliance: Literal['lenient', 'strict'] = 'lenient'
) -> Coding:
    """Parsed a string representing a coding to a Coding object

    Expected format: <namespace_prefix>:<code>

    E.g.:
    >>> parse_coding("SNOMED:404684003", [code_system_module.SNOMED_CT])
    Coding(system=CodeSystem(name=SNOMED CT, name space prefix=SNOMED, version=0.0.0), code='404684003', display='', text='')

    Intended to be called with a list of all resources used.

    Can only recognize the name space prefixes that belong to code systems provided in the resources list. If a name
    space is not found in the resources, it will return a Coding object with the system as the name space prefix and the
    code as the code.

    E.g.:
    >>> parse_coding("SNOMED:404684003", [])
    Warning: Code system with namespace prefix 'SNOMED' not found in resources.
    Warning: Returning Coding object with system as namespace prefix and code as '404684003'
    Coding(system='SNOMED', code='404684003', display='', text='')

    :param coding_str: a string representing a coding
    :param resources: a list of all resources used
    :param compliance: whether to throw a ValueError or just a warning if a name space prefix is not found in the
    resources
    :return: a Coding object as specified in the coding string
    """
    coding_str = coding_str.replace(" ", "")

    if ':' not in coding_str:
        raise ValueError("Invalid coding string, does not contain separator between code and name space prefix: "
                         f"{coding_str}")

    pattern = r'^(.*?):(.*)$'

    match = re.match(pattern, coding_str)

    if match:
        namespace_prefix = match.group(1)  # Part before the colon
        code = match.group(2)  # Part after the colon

        code_system = get_codesystem_by_namespace_prefx(namespace_prefix, resources)

        if code_system:
            return Coding(system=code_system, code=code)
        else:
            if compliance == 'strict':
                raise ValueError(f"Code system with namespace prefix '{namespace_prefix}' not found in resources.")
            else:
                print(f"Warning: Code system with namespace prefix '{namespace_prefix}' not found in resources.")
                coding = Coding(system=namespace_prefix, code=code)
                print(f"Warning: Returning Coding object with system as namespace prefix and code as '{code}'")
                return coding

    else:
        raise ValueError(f"Invalid coding string: {coding_str}")
