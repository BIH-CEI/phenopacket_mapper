from pathlib import Path
from typing import List

from phenopackets.schema.v2 import Phenopacket

from phenopacket_mapper.utils.io import read_phenopackets


class Validator:
    """
    Internal class, implemented using the singleton pattern, that uses phenopacket-tools to validate phenopackets.
    This is complicated a bit by the fact that phenopacket-tools is implemented in java. The singleton pattern ensures
    that only one instance of the class is created for efficiency purposes.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one instance of the class is created."""
        if not cls._instance:
            cls._instance = super(Validator, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        """Initialize the validator only if one is not already initialized."""
        # Initialize only if not already initialized
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # TODO: Implement the validator

    def validate(self, phenopackets: List[Phenopacket]) -> bool:
        """Validate phenopackets using phenopacket-tools.

        :param phenopackets: List of phenopackets to validate
        :return: True if the phenopackets are valid, False otherwise
        """
        # TODO: Implement validation logic
        raise NotImplementedError


def validate(phenopackets: List[Phenopacket]) -> bool:
    """
    Validate phenopackets using phenopacket-tools.

    :param phenopackets: List of phenopackets to validate
    :return: True if the phenopackets are valid, False otherwise
    """
    validator = Validator()
    return validator.validate(phenopackets)


def read_validate(path: Path) -> bool:
    """
    Read phenopackets from a file and validate them.

    :param path: Path to the file containing phenopackets
    :return: True if the phenopackets are valid, False otherwise
    """
    phenopackets = read_phenopackets(path)
    return validate(phenopackets)
