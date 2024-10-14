from phenopacket_mapper.api_requests.hpo_api_request import HPOAPIRequest
from phenopacket_mapper.data_standards import Coding, HPO


def test_hpo_api_request():
    hp = HPOAPIRequest()
    assert hp.get("0000098") == Coding(system=HPO, code="0000098", display="Tall stature")