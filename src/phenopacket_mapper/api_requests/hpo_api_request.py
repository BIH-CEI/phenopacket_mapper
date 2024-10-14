from typing import Union

from phenopacket_mapper.data_standards import CodeSystem
from phenopacket_mapper.api_requests import APIRequestSuperClass
from phenopacket_mapper.api_requests import get as rest_get
from phenopacket_mapper.data_standards import Coding, HPO


class HPOAPIRequest(APIRequestSuperClass):
    """A class to request data from the HPO API."""

    api_base_url = "https://ontology.jax.org/api/hp/terms/HP:"

    def __init__(self, hpo_code_system: CodeSystem = HPO) -> None:
        self.hpo_code_system = hpo_code_system

    def get(self, concept_id: Union[str, int]) -> Coding:
        """Get details about a concept from the Orphanet API."""
        json = rest_get(self.api_base_url + str(concept_id), json=True)

        name = json['name']

        return Coding(
            system=self.hpo_code_system,
            code=str(concept_id),
            display=name
        )
