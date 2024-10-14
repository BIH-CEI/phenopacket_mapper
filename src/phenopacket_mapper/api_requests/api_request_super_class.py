from abc import ABC, abstractmethod

from phenopacket_mapper.data_standards import Coding


class APIRequestSuperClass(ABC):
    """Super class for API requests to get details abput concepts from code systems

    A class should implement this super class to provide a method to get details about a concept from one specific
    code system. An example of this can be seen in `orpha_api_request.py` where the Orphanet API is used to get details
    about a concept from the Orphanet code system.
    """

    @abstractmethod
    def get(self, concept_id) -> Coding:
        pass
