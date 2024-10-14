from phenopacket_mapper.api_requests import OrphaAPIRequest
from phenopacket_mapper.data_standards import Coding, ORDO


def test_orpha_api_request():
    ar = OrphaAPIRequest()
    assert ar.get(95157) == Coding(system=ORDO, code='95157', display='Acute hepatic porphyria')