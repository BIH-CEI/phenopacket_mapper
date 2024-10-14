from dataclasses import dataclass, field
from typing import List, Union, Literal

from phenopacket_mapper.data_standards import CodeSystem, code_system


@dataclass(frozen=True, slots=True, eq=True)
class Coding:
    """Data class for Coding

    A `Coding` is a representation of a concept defined by a code and a code system. It is used in the `CodeableConcept`
    data class.

    :ivar system: The code system that defines the code
    :ivar code: The code that represents the concept
    :ivar display: The human readable representation of the concept
    :ivar text: A human readable description or other additional text of the concept
    """
    system: Union[str, CodeSystem] = field(compare=True)
    code: str = field(compare=True)
    display: str = field(default="", compare=False)
    text: str = field(default="", compare=False)

    @staticmethod
    def parse_coding(
            coding_str: str,
            resources: List[CodeSystem],
            compliance: Literal['lenient', 'strict'] = 'lenient'
    ) -> 'Coding':
        """Parsed a string representing a coding to a Coding object

        Expected format: <namespace_prefix>:<code>

        E.g.:
        >>> Coding.parse_coding("SNOMED:404684003", [code_system.SNOMED_CT])
        Coding(system=CodeSystem(name=SNOMED CT, name space prefix=SNOMED, version=0.0.0), code='404684003', display='', text='')

        Intended to be called with a list of all resources used.

        Can only recognize the name space prefixes that belong to code systems provided in the resources list. If a name
        space is not found in the resources, it will return a Coding object with the system as the name space prefix and the
        code as the code.

        E.g.:
        >>> Coding.parse_coding("SNOMED:404684003", [])
        Warning: Code system with namespace prefix 'SNOMED' not found in resources.
        Warning: Returning Coding object with system as namespace prefix and code as '404684003'
        Coding(system='SNOMED', code='404684003', display='', text='')

        :param coding_str: a string representing a coding
        :param resources: a list of all resources used
        :param compliance: whether to throw a ValueError or just a warning if a name space prefix is not found in the resources
        :return: a Coding object as specified in the coding string
        """
        from phenopacket_mapper.utils.parsing import parse_coding
        return parse_coding(coding_str, resources, compliance)

    def __str__(self):
        return f"{self.system.namespace_prefix}:{self.code} ({self.display})"


@dataclass(frozen=True, slots=True, eq=True)
class CodeableConcept:
    """Data class for CodeableConcept

    A `CodeableConcept` represents a concept that is defined by a set of codes. The concept may additionally have a text
    representation.

    :ivar coding: A list of codings that define the concept
    :ivar text: A text representation of the concept
    """
    coding: List[Coding] = field(compare=True)
    text: str = field(default="", compare=False)
