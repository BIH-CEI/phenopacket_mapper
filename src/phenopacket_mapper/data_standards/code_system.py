from dataclasses import dataclass, replace, field
from typing import List


@dataclass(slots=True, frozen=True)
class CodeSystem:
    """Data class for a CodeSystem

    A `CodeSystem` is a resource that defines a set of codes and their meanings. It could be a terminology, an ontology,
    a nomenclature, etc. Popular examples include SNOMED CT, HPO, MONDO, OMIM, ORDO, LOINC, etc.

    This class is necessary to fill the resources parameter in the Phenopacket later.

    :ivar name: The name of the CodeSystem
    :ivar namespace_prefix: The namespace prefix of the CodeSystem
    :ivar url: The URL of the CodeSystem
    :ivar iri_prefix: The IRI prefix of the CodeSystem
    :ivar version: The version of the CodeSystem
    """
    name: str
    namespace_prefix: str
    url: str = None
    iri_prefix: str = None
    version: str = "0.0.0"
    """List typical alternative abbreviations or names for the resource, to better parse its usage (e.g. 'HPO' for the
    Human Phenotype Ontology, even if its name space prefix is commonly 'HP')"""
    synonyms: List[str] = field(default_factory=lambda: [])

    def set_version(self, value) -> 'CodeSystem':
        return replace(self, version=value)

    def __eq__(self, other):
        """Check if two CodeSystems are equal based on their name, namespace prefix, and version.

        Right now this method ignores the version, this may be subject to change in the future."""
        if not isinstance(other, CodeSystem):
            return False
        return self.namespace_prefix == other.namespace_prefix or self.namespace_prefix in other.synonyms

    def __str__(self):
        return f"CodeSystem(name={self.name}, name space prefix={self.namespace_prefix}, version={self.version})"

    def __repr__(self):
        return str(self)

    def __contains__(self, item):
        from phenopacket_mapper.data_standards import Coding
        if isinstance(item, Coding):
            return self == item.system


NCBITaxon = CodeSystem(
    name='NCBI organismal classification', 
    namespace_prefix='NCBITaxon', 
    url='https://www.ncbi.nlm.nih.gov/taxonomy'
)

GENO = CodeSystem(
    name='GENO: The Genotype Ontology', 
    namespace_prefix='GENO', 
    url='https://www.genoontology.org/'
)

SO = CodeSystem(
    name='Sequence types and features ontology', 
    namespace_prefix='SO',
    url='https://www.sequenceontology.org/'
)

ICD9 = CodeSystem(
    name='International Classification of Diseases, Ninth Revision',
    namespace_prefix='ICD9',
    url='https://www.cdc.gov/nchs/icd/icd9.htm',
    synonyms=['ICD-9', 'ICD_9']
)

ICD10_GM = CodeSystem(
    name='International Classification of Diseases, Tenth Revision, German Modification', 
    namespace_prefix='ICD10GM', 
    url='https://www.bfarm.de/EN/Code-systems/Classifications/ICD/ICD-10-GM/_node.html#:~:text=ICD%20%2D10%2D%20GM%20is%20an,means%20%22German%20Modification%22).',
    synonyms=['ICD10-GM', 'ICD-10-GM', 'ICD10_GM', 'ICD_10_GM']
)

ICD10CM = CodeSystem(
    name='International Classification of Diseases, Tenth Revision, Clinical Modification', 
    namespace_prefix='ICD10CM', 
    url='https://www.cdc.gov/nchs/icd/icd10cm.htm',
    synonyms=['ICD10-CM', 'ICD10_CM', 'ICD-10-CM', 'ICD_10_CM']
)

SNOMED_CT = CodeSystem(
    name='SNOMED CT', 
    namespace_prefix='SNOMED', 
    url='https://www.snomed.org/snomed-ct',
    synonyms=['SCT']
)

ICD11 = CodeSystem(
    name='International Classification of Diseases, Eleventh Revision', 
    namespace_prefix='icd11', 
    url='https://icd.who.int/en',
    synonyms=['ICD-11']
)

HL7FHIR = CodeSystem(
    name='Health Level 7 Fast Healthcare Interoperability Resources', 
    namespace_prefix='HL7FHIR', 
    url='https://www.hl7.org/fhir/'
)

GA4GH = CodeSystem(
    name='Global Alliance for Genomics and Health', 
    namespace_prefix='ga4gh', 
    url='https://www.ga4gh.org/'
)

ISO3166 = CodeSystem(
    name='ISO 3166-1:2020(en) alpha-2 and alpha-3 country codes', 
    namespace_prefix='iso3166', 
    url='https://www.iso.org/iso-3166-country-codes.html'
)

ICF = CodeSystem(
    name='International Classification of Functioning, Disability and Health (ICF)', 
    namespace_prefix='icf', 
    url='https://www.who.int/classifications/icf/en/'
)
MONDO = CodeSystem(
    name="Monarch Disease Ontology",
    namespace_prefix="MONDO",
    url="https://purl.obolibrary.org/obo/mondo.owl"
)
ORDO = CodeSystem(
    name="Orphanet Rare Disease Ontology",
    namespace_prefix="ORPHA",
    url="https://www.orpha.net/",
    synonyms=['ORDO']
)
OMIM = CodeSystem(
    name="Online Mendelian Inheritance",
    namespace_prefix="OMIM",
    url="https://omim.org/"
)
LOINC = CodeSystem(
    name="Logical Observation Identifiers Names and Codes",
    namespace_prefix="LOINC",
    url="https://loinc.org/"
)
HGVS = CodeSystem(
    name="Human Genome Variation Society",
    namespace_prefix="HGVS",
    url="https://varnomen.hgvs.org/"
)
HGNC = CodeSystem(
    name="HUGO Gene Nomenclature Committee",
    namespace_prefix="HGNC",
    url="https://www.genenames.org/"
)
HPO = CodeSystem(
    name="Human Phenotype Ontology",
    namespace_prefix="HP",
    url="https://www.human-phenotype-ontology.org",
    iri_prefix="https://purl.obolibrary.org/obo/HP_",
    synonyms=["HPO"]
)
UO = CodeSystem(
    name="Units of Measurement Ontology",
    namespace_prefix="UO",
    url="https://www.ontobee.org/ontology/UO"
)
NCIT = CodeSystem(
    name = "NCI Thesaurus OBO Edition",
    namespace_prefix = "NCIT",
    url = "https://ncit.nci.nih.gov/"
)

