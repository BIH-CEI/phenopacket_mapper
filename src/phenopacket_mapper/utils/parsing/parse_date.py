import warnings
from datetime import datetime
from typing import Literal, Dict, Tuple, Optional

from phenopacket_mapper.data_standards import Date
from phenopacket_mapper.utils.parsing import parse_int


def parse_date(
        date_str: str,
        default_first: Literal["day", "month"] = "day",
        compliance: Literal['lenient', 'strict'] = 'lenient',
) -> Optional[Date]:
    """Parse a date string into a Date object

    There is a lot of variation in how dates are formatted, and this function attempts to handle as many of them as
    possible. The function will first attempt to parse the date string as an ISO 8601 formatted string. If that fails,
    it will attempt to parse the date string as a date string with separators.

    In this process it is sometimes
    unknowable whether 01-02-2024 is January 2nd or February 1st, so the function will use the `default_first` parameter
    to determine this. If the `default_first` parameter is set to "day", the function will assume that the day comes
    first, and if it is set to "month", the function will assume that the month comes first. If the `default_first`

    :param date_str: the date string to parse
    :param default_first: the default unit to use if it is unclear which unit comes first between day and month
    :param compliance: the compliance level of the parser
    :return: the Date object created from the date string
    """
    separators = ['-', '/', '.']
    # check length
    if len(date_str) < 4:
        raise ValueError(f"Invalid date string '{date_str}': too short")
    elif len(date_str) == 4:
        return Date(year=parse_int(date_str))

    iso_result = Date.from_iso_8601(date_str)

    if iso_result is not None:
        return iso_result

    # try parsing via datetime
    formats = [
        "%Y-%m-%d %H:%M:%S",  # Full date with time
        "%Y-%m-%d",  # Full date without time
        "%d/%m/%Y",  # Day-first format
        "%d.%m.%Y",  # Day-first format with dots
        "%d-%m-%Y",  # Day-first format with dashes
    ]

    for fmt in formats:
        try:
            return Date.from_datetime(datetime.strptime(date_str, fmt))
        except ValueError:
            continue

    # parsing via datetime did not work, interpret like this
    date_str = date_str.replace(" ", "")  # remove spaces

    contains_separators = any([s in date_str for s in separators])

    if contains_separators:
        date_str = date_str.replace('/', '-').replace('.', '-')
        units = date_str.split('-')

        # figure out which units are which
        if len(units) == 2:
            if len(units[0]) == 4:  # year and month
                return Date(year=parse_int(units[0]), month=parse_int(units[1]))
            else:  # month and year
                return Date(year=parse_int(units[1]), month=parse_int(units[0]))
        elif len(units) == 3:
            if len(units[0]) == 4:
                day, month = _wrapper__most_likely_date_and_month(
                    units[1], units[2],
                    date_str, default_first, compliance
                )
                return Date(year=parse_int(units[0]), month=month, day=day)
            elif len(units[1]) == 4:
                day, month = _wrapper__most_likely_date_and_month(
                    units[0], units[2],
                    date_str, default_first, compliance
                )
                return Date(year=parse_int(units[1]), month=month, day=day)
            elif len(units[2]) == 4:
                day, month = _wrapper__most_likely_date_and_month(
                    units[0], units[1],
                    date_str, default_first, compliance
                )
                return Date(year=parse_int(units[2]), month=month, day=day)

    else:
        if compliance == 'strict':
            raise ValueError(f"Invalid date string '{date_str}': no separators found")
        else:
            warnings.warn(f"Invalid date string '{date_str}': could not be parsed, returning None")
            return None


def _wrapper__most_likely_date_and_month(
        str0: str,
        str1: str,
        full_date_str: str,
        default_first: Literal["day", "month"] = "day",
        compliance: Literal['lenient', 'strict'] = 'lenient'
) -> Tuple[int, int]:
    """
    Wrapper for _return_most_likely_date_and_month that raises an error if the compliance is set to 'strict'

    returns the day and month from the most likely date and month from two strings

    :param str0: the first string
    :param str1: the second string
    :param full_date_str: the full date string
    :param default_first: the default unit to use if it is unclear which unit comes first between day and month
    :param compliance: the compliance level of the parser
    :return: the day and month from the most likely date and month from two strings
    """
    result = _return_most_likely_date_and_month(str0, str1, full_date_str, default_first)
    if result['inference'] and compliance == 'strict':
        raise ValueError(f"Invalid date string '{full_date_str}': unclear which unit of time is first")
    day = result['day']
    month = result['month']
    return day, month


def _return_most_likely_date_and_month(
        str0: str,
        str1: str,
        full_date_str: str,
        default_first: Literal["day", "month"] = "day"
) -> Dict[str, int]:
    """
    Return the most likely date and month from two strings

    Given two strings, return the most likely day and month from them. The formatting of the output is
    {'day': day, 'month': month} where date and month are integers.

    :param str0: the first string
    :param str1: the second string
    :return: the most likely day and month from the two strings
    """
    int0 = parse_int(str0)
    int1 = parse_int(str1)

    if not isinstance(int0, int):
        raise ValueError(f"Invalid date string '{full_date_str}': {str0} is not a valid number")
    if not isinstance(int1, int):
        raise ValueError(f"Invalid date string '{full_date_str}': {str1} is not a valid number")

    if int0 > 12 >= int1:
        return {'day': int0, 'month': int1, 'inference': False}
    elif int0 <= 12 < int1:
        return {'day': int1, 'month': int0, 'inference': False}
    else:  # unclear which is which, fall back on default
        print(f"WARNING: unclear which unit of time is first in date string: {full_date_str}, "
              f"falling back on default: {default_first} for parsing date.")
        if default_first == "day":
            return {'day': int0, 'month': int1, 'inference': True}
        elif default_first == "month":
            return {'day': int1, 'month': int0, 'inference': True}
        else:
            raise ValueError(f"Invalid default_first value: {default_first}")
