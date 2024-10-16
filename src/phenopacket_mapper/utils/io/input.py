import math
import os
from io import IOBase
from pathlib import Path
from types import MappingProxyType
from typing import Literal, List, Union, Dict, Tuple

import pandas as pd
from phenopackets.schema.v2 import Phenopacket
from google.protobuf.json_format import Parse

from phenopacket_mapper.data_standards import DataModel, DataModelInstance, DataField, CodeSystem, DataFieldValue, \
    DataSet
from phenopacket_mapper.utils import loc_default
from phenopacket_mapper.utils import parsing
from phenopacket_mapper.utils.io.data_reader import DataReader
from phenopacket_mapper.utils.parsing import parse_ordinal


def read_data_model(
        data_model_name: str,
        resources: List[CodeSystem],
        path: Union[str, Path],
        file_type: Literal['csv', 'excel', 'unknown'] = 'unknown',
        column_names: Dict[str, str] = MappingProxyType({
            DataField.name.__name__: 'data_field_name',
            DataField.description.__name__: 'description',
            DataField.specification.__name__: 'value_set',
            DataField.required.__name__: 'required',
        }),
        parse_value_sets: bool = False,
        remove_line_breaks: bool = False,
        parse_ordinals: bool = True,
) -> DataModel:
    """Reads a Data Model from a file

    :param data_model_name: Name to be given to the `DataModel` object
    :param resources: List of `CodeSystem` objects to be used as resources in the `DataModel`
    :param path: Path to Data Model file
    :param file_type: Type of file to read, either 'csv' or 'excel'
    :param column_names: A dictionary mapping from each field of the `DataField` (key) class to a column of the file
                        (value). Leaving a value empty (`''`) will leave the field in the `DataModel` definition empty.
    :param parse_value_sets: If True, parses the string to a ValueSet object, can later be used to check
                        validity of the data. Optional, but highly recommended.
    :param remove_line_breaks: Whether to remove line breaks from string values
    :param parse_ordinals: Whether to extract the ordinal number from the field name. Warning: this can overwrite values
                             Ordinals could look like: "1.1.", "1.", "I.a.", or "ii.", etc.
    """
    if isinstance(column_names, MappingProxyType):
        column_names = dict(column_names)
    if file_type == 'unknown':
        file_type = path.suffix[1:]

    if file_type == 'csv':
        df = pd.read_csv(path)
    elif file_type == 'excel':
        df = pd.read_excel(path)
    else:
        raise ValueError('Unknown file type')

    # Change NaN values to None
    df = df.where(pd.notnull(df), None)

    def invert_dict(d: Dict) -> Dict:
        return {v: k for k, v in d.items()}

    # invert column names
    inv_column_names = invert_dict(column_names)

    # remove empty assignments
    inv_column_names = {k: inv_column_names[k] for k in list(filter(lambda x: x != '', inv_column_names.keys()))}

    # check that column_names.keys() is a subsets of the columns in the file
    df_columns = list(df)
    print(f"{df_columns=}")
    keep = []
    for col_n in inv_column_names.keys():
        if col_n in df_columns:
            keep.append(col_n)

    inv_column_names = {k: inv_column_names[k] for k in keep}

    if len(inv_column_names) == 0:
        raise ValueError("The column names dictionary that was passed is invalid.")

    for col in inv_column_names.keys():
        print(f"Column {col} maps to DataField.{inv_column_names[col]}")

    column_names = invert_dict(inv_column_names)

    def remove_line_breaks_if_not_none(value):
        if value is not None:
            return value.replace('\n', ' ')
        return value

    data_fields: Tuple[DataField, ...] = tuple()
    for i in range(len(df)):
        data_field_name = loc_default(df, row_index=i, column_name=column_names.get(DataField.name.__name__, ''))
        value_set = loc_default(df, row_index=i, column_name=column_names.get(DataField.specification.__name__, ''))
        description = loc_default(df, row_index=i, column_name=column_names.get(DataField.description.__name__, ''))
        required = bool(loc_default(df, row_index=i, column_name=column_names.get(DataField.required.__name__, '')))

        if remove_line_breaks:
            data_field_name = remove_line_breaks_if_not_none(data_field_name)
            description = remove_line_breaks_if_not_none(description)

        if parse_ordinals:
            ordinal, data_field_name = parse_ordinal(data_field_name)

        if parse_value_sets:
            if not column_names.get(DataField.specification.__name__, ''):
                raise ValueError("Value set column name must be provided to parse value sets.")

            value_set = parsing.parse_value_set(
                value_set_str=value_set,
                value_set_name=f"Value set for '{data_field_name}' field",
                resources=resources
            )

        data_fields = data_fields + (
            DataField(
                name=data_field_name,
                specification=value_set,
                description=description,
                required=required,
            ),
        )

    return DataModel(data_model_name=data_model_name, fields=data_fields, resources=resources)


def load_tabular_data_using_data_model(
        file: Union[str, Path, IOBase, List[str], List[Path], List[IOBase]],
        data_model: DataModel,
        column_names: Dict[str, str],
        compliance: Literal['lenient', 'strict'] = 'lenient',
) -> DataSet:
    """Loads data from a file using a DataModel definition

    List a column for each field of the `DataModel` in the `column_names` dictionary. The keys of the dictionary should
    be {id}_column for each field and the values should be the name of the column in the file.

    E.g.:
    ```python
    data_model = DataModel("Test data model", [DataField(name="Field 1", value_set=ValueSet())])
    column_names = {"field_1_column": "column_name_in_file"}
    load_data_using_data_model("data.csv", data_model, column_names)
    ```

    :param file:
    :param data_model: DataModel to use for reading the file
    :param column_names: A dictionary mapping from the id of each field of the `DataField` to the name of a
                        column in the file
    :param compliance: Compliance level to enforce when reading the file. If 'lenient', the file can have extra fields
                        that are not in the DataModel. If 'strict', the file must have all fields in the DataModel.
    :return: List of DataModelInstances
    """
    dr = DataReader(file)
    data, data_iterable = dr.data, dr.iterable

    df = data

    # check column_names is in the correct format
    if isinstance(column_names, MappingProxyType):
        column_names = dict(column_names)
    for f in data_model.fields:
        if f.id not in column_names.keys() and f.id + "_column" not in column_names.keys():
            raise ValueError(f"Column name for field id: {f.id} name: {f.name} not found in column_names dictionary,"
                             f" list it with the key '{f.id}_column'")
        elif f.id + "_column" in column_names.keys():
            column_names[f.id] = column_names.pop(f.id + "_column")

    data_model_instances = []

    for i in range(len(df)):
        values = []
        for f in data_model.fields:
            column_name = column_names[f.id]

            pandas_value = loc_default(df, row_index=i, column_name=column_name)

            if not pandas_value or (isinstance(pandas_value, float) and math.isnan(pandas_value)):
                continue

            value_str = str(pandas_value)
            value = parsing.parse_value(value_str=value_str, resources=data_model.resources, compliance=compliance)
            values.append(DataFieldValue(row_no=i, field=f, value=value))
        data_model_instances.append(
            DataModelInstance(
                row_no=i,
                data_model=data_model,
                values=values,
                compliance=compliance)
        )

    return DataSet(data_model=data_model, data=data_model_instances)


def read_phenopackets(dir_path: Path) -> List[Phenopacket]:
    """Reads a list of Phenopackets from JSON files in a directory.

    :param dir_path: The directory containing JSON files.
    :type dir_path: Union[str, Path]
    :return: The list of loaded Phenopackets.
    :rtype: List[Phenopacket]
    """
    phenopackets_list = []
    for file_name in os.listdir(dir_path):
        if file_name.endswith('.json'):
            file_path = os.path.join(dir_path, file_name)
            phenopacket = read_phenopacket_from_json(file_path)
            phenopackets_list.append(phenopacket)
    return phenopackets_list


def read_phenopacket_from_json(path: Union[str, Path]) -> Phenopacket:
    """Reads a Phenopacket from a JSON file.

    :param path: The path to the JSON file.
    :type path: Union[str, Path]
    :return: The loaded Phenopacket.
    :rtype: Phenopacket
    """
    with open(path, 'r') as fh:
        json_data = fh.read()
        phenopacket = Phenopacket()
        Parse(json_data, phenopacket)
        return phenopacket
