[![Build status](https://github.com/bih-cei/phenopacket_mapper/workflows/CI/badge.svg)](https://github.com/bih-cei/phenopacket_mapper/actions/workflows/python_ci.yml) [![Coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/frehburg/67304fe3700ce3d41079e75f4fe9609f/raw/phenopacket_mapper_test_cov.JSON)](https://github.com/bih-cei/phenopacket_mapper/actions/workflows/python_ci.yml) [![LOCs](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/frehburg/25d4f4d4d222fcb5f266a280b1dd60d4/raw/phenopacket_mapper_locs.JSON)](https://github.com/bih-cei/phenopacket_mapper/actions/workflows/locs.yml)

[Stable Documentation](https://bih-cei.github.io/phenopacket_mapper/stable/)  
[Latest Documentation](https://bih-cei.github.io/phenopacket_mapper/latest/)  

# Phenopacket Mapper

A Python library to map from any bespoke tabular data format to the GA4GH Phenopacket schema.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
- [Features](#features)
- [Contributing](#contributing)
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
gap between the bespoke tabular data formats and the Phenopacket schema. It provides a way to map from any bespoke tabular
data format to the GA4GH Phenopacket schema with a simple configuration.

## Features

List the key features of your project.

## Getting Started

Instructions on how to set up and run your project locally.

### Prerequisites

List any software, libraries, or dependencies that need to be installed before setting up the project.

### Installation

Step-by-step instructions on how to install and set up your project.

To install your own code run `pip install -e .` in a terminal

## Features

Run `pm -h`

```
Usage: pm [-h] {quickstart,mapping,validate} ...

 Phenopacket Mapper (pm) CLI tool.

positional arguments:
  {quickstart,mapping,validate}
                        Available commands
    quickstart          Generate a notebook with sample code.
    mapping             Execute the mapping.
    validate            Validate phenopackets.

options:
  -h, --help            show this help message and exit
```

## Contributing

Guidelines for contributing to your project. Include information about how others can contribute, submit issues, and create pull requests.

## License

Specify the license under which your project is distributed.

## Acknowledgements
This is a part of the larger effort conducted in the  repository [ GitHub Repository](www.github.com/bih-cei/)
