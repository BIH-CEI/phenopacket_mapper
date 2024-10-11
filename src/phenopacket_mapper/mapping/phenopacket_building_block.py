from typing import Union, Dict

from phenopackets.schema.v2.core.base_pb2 import OntologyClass
from google.protobuf.timestamp_pb2 import Timestamp

from phenopacket_mapper.data_standards import DataModelInstance, DataField, DataFieldValue, Coding


class PhenopacketBuildingBlock:

    def __init__(self, phenopacket_element, **kwargs):
        """Mapping equivalent to the constructor of a Phenopacket element (e.g., Individual) for the mapping

        List fields of the Phenopacket element constructor in the kwargs to map the data to Phenopackets.

        :param phenopacket_element: The phenopacket element to map to (e.g., `phenopackets.Individual`)
        :param kwargs: The elements to map the data to Phenopackets
        """
        self.phenopacket_element = phenopacket_element
        self.elements: Dict[str, Union[PhenopacketBuildingBlock, DataField]] = {}
        for k, v in kwargs.items():
            setattr(self, k, v)
            self.elements[k] = v

    def map(self, instance: DataModelInstance):
        """Creates the phenopacket element by the mapping specified in fields

        >>> import phenopackets
        >>> from phenopacket_mapper.data_standards import DataModelInstance, DataModel, DataField, DataFieldValue
        >>> data_field = DataField("pseudonym", str)
        >>> data_model = DataModel("Example data model", [data_field], [])
        >>> inst = DataModelInstance(0, data_model, [DataFieldValue(0, data_field, "example_pseudonym")])
        >>> individual = PhenopacketBuildingBlock(phenopackets.Individual, id=data_field).map(inst)
        >>> individual.id
        'example_pseudonym'

        :param instance: the `DataModelInstance` from which to map to a Phenopacket schema element
        :return: the resulting Phenopacket schema element
        """
        kwargs = {}
        for key, e in self.elements.items():
            map_single(key, e, instance, kwargs)

        return self.phenopacket_element(**kwargs)


def map_single(key, e, instance: DataModelInstance, kwargs):
    if isinstance(e, DataField):
        data_field = e
        try:
            value: DataFieldValue = getattr(instance, data_field.id).value

            from phenopacket_mapper.data_standards import Date
            if isinstance(value, Date):
                date = value
                timestamp = date.protobuf_timestamp()
                assert isinstance(timestamp, Timestamp)
                kwargs[key] = timestamp
            elif isinstance(value, Coding):
                kwargs[key] = OntologyClass(id=str(value), label=value.display)
            else:
                kwargs[key] = value
        except AttributeError:
            pass
    elif isinstance(e, list):
        kwargs[key] = [v.map(instance) for v in e]
    elif isinstance(e, PhenopacketBuildingBlock):
        phenopacket_element = e
        kwargs[key] = phenopacket_element.map(instance)
