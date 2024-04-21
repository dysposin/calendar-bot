import datetime
from typing import Optional


def parse_date(date_string: str, delimiter: str=".") -> Optional[datetime.date]:
    """
    Parses a string into a date object, return None if it doesn't match format.
    Missing elements are replaced by current month and/or year.

    >>> parse_date("11.2.2003")
    datetime.date(2003, 2, 11)
    >>> parse_date("11.2.") is not None
    True
    >>> parse_date("11") is not None
    True
    >>> parse_date("32.10.")
    None
    """
    today = datetime.datetime.now()
    month = today.month
    year = today.year
    try:
        elements = date_string.rstrip('.').split(delimiter, 3)
        match len(elements):
            case 1:
                day = int(elements[0])
            case 2:
                day, month = list(map(int, elements))
            case 3:
                day, month, year = list(map(int, elements))

        return datetime.date(year, month, day)
    except (ValueError, AttributeError):
            pass
    return None


def parse_time(date_string: str, delimiter: str=":") -> Optional[datetime.date]:
    """
    Parses a string into a datetime object, return None if it doesn't match format.
    Missing elements are replaced by current month and/or year.
    >>> parse_time("12:13")
    datetime.time(12, 13)
    >>> parse_time("12")
    datetime.time(12, 0)
    >>> parse_time("25:12")
    None
    """
    minutes = 0
    try:
        elements = date_string.split(delimiter, 2)
        match len(elements):
            case 1:
                hour = list(map(int, elements))
            case 2:
                hour, minutes = list(map(int, elements))

        return datetime.time(hour, minutes)
    except (ValueError, AttributeError):
            pass
    return None


def parse_date_range(date_string: str) -> tuple[Optional[datetime.date], Optional[datetime.date]]:
    """
    Checks if given string is a valid range of dates, returns a tuple of date objects or 
    None if the date isn't valid.

    >>> parse_date_range("1.1.1-2.2.2")
    (datetime.date(1, 1, 1), datetime.date(2, 2, 2))
    >>> parse_date_range("1.1.1")
    (datetime.date(1, 1, 1), None)
    >>> parse_date_range("abc")
    (None, None)
    >>> parse_date_range("abc-2.2.2")
    (None, datetime.date(2, 2, 2))
    """

    try:
        date_start, date_end = date_string.split("-")
    except ValueError:
        date_start, date_end = date_string, None
    
    # in case the month/year is defined only on one of the dates, e.g. 1.-2.3.1900
    elements_start = date_start.split(".")
    elements_end = date_end.split(".")
    delta = len(elements_end) - len(elements_start)
    if delta > 0:
        elements_start.extend(elements_end[3 - delta:])
    elif delta < 0:
        elements_end.extend(elements_start[3 - delta:])

    if elements_start[-1] < 2000:
        elements_start[-1] += 2000
    if elements_end[-1] < 2000:
        elements_end[-1] += 2000
    date_start = ".".join(elements_start)
    date_end = ".".join(elements_end)

    date_start = parse_date(date_start)
    date_end = parse_date(date_end)

    return date_start, date_end


def parse_time_range(time_string: str) -> tuple[Optional[datetime.time], Optional[datetime.time]]:
    """
    Checks if given string is a valid range of times, returns a tuple of time objects or 
    None if the time isn't valid.

    >>> parse_time_range("10:02-10:32")
    datetime.time(10, 2), datetime.time(10, 21)
    >>> parse_time_range("10:02-asd")
    datetime.time(10, 2), None
    """
    try:
        time_start, time_end = time_string.split("-")
    except ValueError:
        time_start, time_end = time_string, None
    time_start = parse_time(time_start)
    time_end = parse_time(time_end)

    return time_start, time_end


def parse_message(message, delimiter: str=',', parameter_count: int=4) -> tuple:
    """

    """
    command, parameters = message.split(" ")
    parameters = parameters.split(delimiter, parameter_count)
    return command, parameters
