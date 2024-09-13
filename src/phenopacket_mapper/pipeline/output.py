import os
from pathlib import Path
from typing import List, Union

from google.protobuf.json_format import MessageToJson
from phenopackets.schema.v2 import Phenopacket


def write(
        phenopackets_list: List[Phenopacket], out_dir: Union[str, Path]
) -> None:
    """Writes a list of phenopackets to JSON files.

    :param phenopackets_list: The list of phenopackets.
    :type phenopackets_list: List[Phenopacket]
    :param out_dir: The output directory.
    :type out_dir: Union[str, Path]
    """
    # Make sure output out_dr exists.
    os.makedirs(out_dir, exist_ok=True)

    for phenopacket in phenopackets_list:
        _write_single_phenopacket(phenopacket, out_dir)


def _write_single_phenopacket(
        phenopacket: Phenopacket,
        out_dr: Union[str, Path]
) -> None:
    """Writes a phenopacket to a JSON file.

    :param phenopacket: The phenopacket.
    :type phenopacket: Phenopacket
    :param out_dr: The output directory.
    :type out_dr: Union[str, Path]
    """
    json_str = MessageToJson(phenopacket)  # Convert phenopacket to JSON string.
    out_path = os.path.join(out_dr, (phenopacket.id + '.json'))
    with open(out_path, 'w') as fh:
        fh.write(json_str)
