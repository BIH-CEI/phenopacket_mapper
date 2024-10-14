from typing import Union

from bs4 import BeautifulSoup

from phenopacket_mapper.data_standards import CodeSystem
from phenopacket_mapper.api_requests import APIRequestSuperClass
from phenopacket_mapper.api_requests import get as rest_get
from phenopacket_mapper.data_standards import Coding, ORDO


class OrphaAPIRequest(APIRequestSuperClass):
    """A class to request data from the Orphanet API."""

    api_base_url = "https://www.orpha.net/en/disease/detail/"

    def __init__(self, orpha_code_system: CodeSystem = ORDO) -> None:
        self.orpha_code_system = orpha_code_system

    def get(self, concept_id: Union[str, int]) -> Coding:
        """Get details about a concept from the Orphanet API."""
        html = rest_get(self.api_base_url + str(concept_id))

        soup = BeautifulSoup(html, 'html.parser')

        title = soup.title.string.replace("Orphanet: ", "")

        return Coding(
            system=self.orpha_code_system,
            code=str(concept_id),
            display=title
        )
