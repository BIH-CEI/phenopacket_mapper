from typing import Union


def parse_primitive_data_value(
        value_str: str
) -> Union[str, bool, int, float]:
    """Parses an int, float, bool, or string from a string value.

    Relies on the inbuilt Python type conversion functions to parse the value_str.

    :param value_str: The string value to be parsed.
    :return: The parsed value as an int, float, bool, or string.
    """
    # 1. Check if the value_str is a string
    if not isinstance(value_str, str):
        raise ValueError(f"Value must be a string, not {type(value_str)}")

    # 2. Check if the value_str is an int, float, or bool
    parsing_functions = [parse_int, parse_float, parse_bool]

    for parsing_func in parsing_functions:
        value = parsing_func(value_str)
        if value is not None:
            return value

    # 3. Return the value_str as a string (definitely not an int, float, or bool, but is a string)
    return value_str


def parse_int(int_str: str) -> Union[int, None]:
    """Parses an int from a string value.

    If the string value cannot be parsed as an int, None is returned.

    :param int_str: The string value to be parsed.
    :return: The parsed value as an int. Or None if the string value cannot be parsed as an int.
    """
    int_str = int_str.replace(" ", "")  # remove spaces

    try:
        return int(int_str)
    except ValueError:
        return None


def parse_float(float_str: str) -> Union[float, None]:
    """Parses a float from a string value.

    If the string value cannot be parsed as a float, None is returned.

    :param float_str: The string value to be parsed.
    :return: The parsed value as a float. Or None if the string value cannot be parsed as a float.
    """
    float_str = float_str.replace(" ", "")  # remove spaces

    try:
        return float(float_str)
    except ValueError:
        return None


def parse_bool(bool_str: str) -> Union[bool, None]:
    """Parses a boolean from a string value.

    If the string value cannot be parsed as a boolean, None is returned.

    On purpose does not parse 0 and 1 to False and True respectively, to avoid confusion with numeric values.

    :param bool_str: The string value to be parsed.
    :return: The parsed value as a boolean. Or None if the string value cannot be parsed as a boolean.
    """
    bool_str = bool_str.replace(" ", "")  # remove spaces

    if bool_str.lower() == "true" or bool_str.lower() == "t":
        return True
    if bool_str.lower() == "false" or bool_str.lower() == "f":
        return False
