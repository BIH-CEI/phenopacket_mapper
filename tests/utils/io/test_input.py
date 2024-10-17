from io import StringIO

import pytest

from phenopacket_mapper import DataModel
from phenopacket_mapper.data_standards import DataField, Cardinality, ValueSet, DataSection, OrGroup, DataFieldValue
from phenopacket_mapper.data_standards.data_model import DataSectionInstance, DataModelInstance
from phenopacket_mapper.utils.io import DataReader
from phenopacket_mapper.utils.io.input import load_hierarchical_data_recursive, load_hierarchical_data


@pytest.fixture
def buffer():
    xml_data = (
        '<?xml version="1.0" encoding="UTF-8" ?> <ODM xmlns="http://www.cdisc.org/ns/odm/v1.3" xmlns:ds="http://www.w3.org/2000/09/xmldsig#" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:redcap="https://projectredcap.org" xsi:schemaLocation="http://www.cdisc.org/ns/odm/v1.3 schema/odm/ODM1-3-1.xsd" ODMVersion="1.3.1" FileOID="000-00-0000" FileType="Snapshot" Description="genAdipositas - ALT Demo" AsOfDateTime="2024-10-14T11:57:18" CreationDateTime="2024-10-14T11:57:18" SourceSystem="REDCap" SourceSystemVersion="14.6.9"> '
        '<ClinicalData StudyOID="Project.GenAdipositasALTDemo" MetaDataVersionOID="Metadata.GenAdipositasALTDemo_2024-10-14_1157">'
        '<SubjectData SubjectKey="101" redcap:RecordIdField="record_id">'
        '<ANumber>123</ANumber>'
        '</SubjectData>'
        '</ClinicalData>'
        '</ODM>'
    )
    return StringIO(xml_data)


@pytest.fixture
def genomic_interpretation():
    return DataModel(
        name="Phenopacket schema Genomic Interpretation",
        fields=(
            DataField(
                name="subject_or_biosample_id",
                specification=int,
                required=True,
                description="The id of the patient or biosample that is the subject being interpreted. REQUIRED.",
                cardinality=Cardinality.ONE,
            ),

            DataField(
                name="interpretation_status",
                specification=ValueSet(
                    name="Interpretation Status Value Set",
                    elements=("UNKNOWN_STATUS", "REJECTED", "CANDIDATE", "CONTRIBUTORY", "CAUSATIVE"),
                ),
                required=True,
                description="status of the interpretation. REQUIRED.",
            ),

            DataSection(
                name="example",
                required=True,
                fields=(
                    DataField(
                        name="a_number",
                        required=True,
                        specification=int,
                    ),
                )
            ),

            OrGroup(
                name="call",
                fields=(
                    DataSection(
                        name="GeneDescriptor",
                        fields=(
                            DataField(
                                name="value_id",
                                specification=str,
                                required=True,
                                description="Official identifier of the gene. REQUIRED."
                            ),

                            DataField(
                                name="symbol",
                                specification=str,
                                required=True,
                                description="Official gene symbol. REQUIRED."
                            ),

                            DataField(
                                name="description",
                                specification=str,
                                required=False,
                                description="A free-text description of the gene"
                            ),
                        ),
                    ),
                ),
            ),
        )
    )


def test_load_hierarchical_data_recursive_xml_genomic_interpretation_example_datafieldvalue(buffer, genomic_interpretation):
    data_reader = DataReader(
        file=buffer,
        file_extension="xml",
    )
    assert load_hierarchical_data_recursive(
        loaded_data_instance_identifier="TEST_IDENTIFIER",
        loaded_data_instance=data_reader.data,
        data_model=genomic_interpretation.subject_or_biosample_id,
        compliance='strict',
        mapping={
            genomic_interpretation.subject_or_biosample_id: "ODM.ClinicalData.SubjectData.SubjectKey",
            genomic_interpretation.example.a_number: "ODM.ClinicalData.SubjectData.ANumber",
        },
        resources=tuple(),
    ) == DataFieldValue(
        id="TEST_IDENTIFIER:ODM.ClinicalData.SubjectData.SubjectKey",
        value=101,
        field=genomic_interpretation.subject_or_biosample_id,
    )


def test_load_hierarchical_data_recursive_xml_genomic_interpretation_example_datasection(
        buffer,
        genomic_interpretation
):
    data_reader = DataReader(
        file=buffer,
        file_extension="xml",
    )
    assert load_hierarchical_data_recursive(
        loaded_data_instance_identifier="TEST_IDENTIFIER",
        loaded_data_instance=data_reader.data,
        data_model=genomic_interpretation.example,
        compliance='strict',
        mapping={
            genomic_interpretation.subject_or_biosample_id: "ODM.ClinicalData.SubjectData.SubjectKey",
            genomic_interpretation.example.a_number: "ODM.ClinicalData.SubjectData.ANumber",
        },
        resources=tuple(),
    ) == DataSectionInstance(
        id="TEST_IDENTIFIER:example",
        section=genomic_interpretation.example,
        values=(
            DataFieldValue(
                id='TEST_IDENTIFIER:ODM.ClinicalData.SubjectData.ANumber',
                field=genomic_interpretation.example.a_number,
                value=123
            ),
        )
    )


def test_load_hierarchical_data_xml_genomic_interpretation_example_instance(buffer, genomic_interpretation):
    assert load_hierarchical_data(
        file=buffer,
        file_extension="xml",
        data_model=genomic_interpretation,
        compliance='strict',
        mapping={
            genomic_interpretation.subject_or_biosample_id: "ODM.ClinicalData.SubjectData.SubjectKey",
            genomic_interpretation.example.a_number: "ODM.ClinicalData.SubjectData.ANumber",
        },
    ) == DataModelInstance(
        id="PLACEHOLDER_IDENTIFIER",    # TODO: change once correct identifier is available
        data_model=genomic_interpretation,
        compliance='strict',
        values=(
            DataFieldValue(
                id="PLACEHOLDER_IDENTIFIER:ODM.ClinicalData.SubjectData.SubjectKey",  # TODO: change once correct identifier is available
                value=101,
                field=genomic_interpretation.subject_or_biosample_id,
            ),
            DataSectionInstance(
                id="PLACEHOLDER_IDENTIFIER:example",  # TODO: change once correct identifier is available
                section=genomic_interpretation.example,
                values=(
                    DataFieldValue(
                        id='PLACEHOLDER_IDENTIFIER:ODM.ClinicalData.SubjectData.ANumber',  # TODO: change once correct identifier is available
                        field=genomic_interpretation.example.a_number,
                        value=123
                    ),
                )
            ),
        )
    )
