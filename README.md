[![Build status](https://github.com/bih-cei/phenopacket_mapper/workflows/CI/badge.svg)](https://github.com/bih-cei/phenopacket_mapper/actions/workflows/python_ci.yml)

[Stable Documentation](https://bih-cei.github.io/phenopacket_mapper/stable/)  
[Latest Documentation](https://bih-cei.github.io/phenopacket_mapper/latest/)  

# Phenopacket Mapper

A Python library to map from any bespoke tabular data format to the GA4GH Phenopacket schema.

![Mapping Flow](res/imgs/docs/phenopacket_mapper_flow_simplified.png)

## Table of Contents

- [Motivation](#motivation)
- [Features](#features)
- [Installation](#installation)
- [User Guides](#user-guides)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Motivation

The Phenopacket schema is a standard for representing phenotypic data in a structured way. This enables the exchange of 
phenotypic data between different systems and tools. Further, the schema's structured format enables machine-readability
and -interpretability. Approaches such as [Genotypes and Phenotypes - Statistical Evaluation of Associations (GPSEA)](https://github.com/monarch-initiative/gpsea)
leverage the Phenopacket schema to perform statistical analyses on phenotypic data. Future work will enable machine learning
models to be trained on phenotypic data in the Phenopacket format.

For the feasibility of such studies, it is imperative that data be available in the Phenopacket format. However, it is
common to find data in bespoke tabular formats at the point of creation and storage. Since the operators who generate
the data are often clinicians or researchers, it is not to be expected of them to furthermore be proficient programmers.
The Phenopacket schema brings with it a learning curve that is not trivial to overcome. This library aims to bridge the
gap between the bespoke tabular data formats and the Phenopacket schema by making the creation of phenopackets intuitive
and easy to use.

## Features
Please read the [latest documentation](https://bih-cei.github.io/phenopacket_mapper/latest/introduction.html).

## Installation

Please read the [latest documentation](https://bih-cei.github.io/phenopacket_mapper/latest/installation.html).



## User Guides
1. [Quickstart](https://bih-cei.github.io/phenopacket_mapper/stable/quickstart)
2. etc

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
This is a part of the larger effort in collaboration with Adam Graefe, Daniel Danis, and Peter Robinson.

```
   [![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/frehburg/67304fe3700ce3d41079e75f4fe9609f/raw/phenopacket_mapper_test_cov.JSON)](https://github.com/bih-cei/phenopacket_mapper/actions/workflows/python_ci.yml) [![LOCs](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/frehburg/25d4f4d4d222fcb5f266a280b1dd60d4/raw/phenopacket_mapper_locs.JSON)](https://github.com/bih-cei/phenopacket_mapper/actions/workflows/locs.yml))
```
