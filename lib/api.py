import datetime
from lib import parsers, calendar, event


def add(parameters: list[str], event_calendar: calendar.Calendar, parameter_count: int=4):
    """
    Add an event to a given calendar.

    parameters (list[str]): list of parameters for the event
    event_calendar (calendar.Calendar): calendar to update
    parameter_count (int): number of expected parameters
    """
    # Pad the parameters list
    padding = [None]*(parameter_count - len(parameters))
    parameters.expand(padding)

    author, datestring, timestring, title, info = parameters

    date_start, date_end = parsers.parse_date_range(datestring)
    time_start, time_end = parsers.parse_time_range(timestring)

    clock = time_start is not None or time_end is not None

    time_start_default = datetime.time(0, 0)
    time_end_default = datetime.time(23, 59)
    match date_start, date_end, time_start, time_end:
        case _, None, None, None:
            # Only start date given, default end date and start and end times are the same day 00:00 and 23:59
            date_start = datetime.datetime.combine(date_start, time_start_default)
            date_end = datetime.datetime.combine(date_start, time_end_default)
        case _, _, None, None:
            # Start and end date given, default start and end times are 00:00 and 23:59
            date_start = datetime.datetime.combine(date_start, time_start_default)
            date_end = datetime.datetime.combine(date_end, time_end_default)
        case _, None, _, None:
            # Start date and time given, default end date and time is 23:59 the same day
            date_start = datetime.datetime.combine(date_start, time_start)
            date_end = datetime.datetime.combine(date_start, time_end_default)
        case _, None, None, _:
            # Start date and end time given, default end date and start time are 00:00 the same day
            date_start = datetime.datetime.combine(date_start, time_start_default)
            date_end = datetime.datetime.combine(date_start, time_end)
        case _, _, _, None:
            # Start and end date and start time given, default end time is 23:59
            date_start = datetime.datetime.combine(date_start, time_start)
            date_end = datetime.datetime.combine(date_end, time_end_default)
        case _, _, None, _:
            # Start and end date and en time given, default start time is 00:00 starting day
            date_start = datetime.datetime.combine(date_start, time_start_default)
            date_end = datetime.datetime.combine(date_start,  time_end)
        case _, None, _, _:
            # Start date and start and end time given, default end date is the same day
            date_start = datetime.datetime.combine(date_start, time_start)
            date_end = datetime.datetime.combine(date_start, time_end)
        case _, _, None, _:
            # Start and end date and  end time given, default start time is 00:00
            date_start = datetime.datetime.combine(date_start, time_start)
            date_end = datetime.datetime.combine(date_start, time_end)
        case _, _, _, _:
            # All parameters given
            date_start = datetime.datetime.combine(date_start, time_start)
            date_end = datetime.datetime.combine(date_end,  time_end)
        case _:
            raise ValueError("Couldn't parse event date parameters")
    new_event = event.Event(author, title, date_start, date_end, info, clock)
    event_calendar.add_event(new_event)


def remove(search_term: str, calendar: calendar.Calendar):
    """
    Remove event if search term returns only one result, otherwise return all found events.

    search_term (str): Search term used to find events
    calendar (calendar.Calendar): The calendar in use
    """
    events = calendar.search(search_term)
    match len(events):
        case 1:
            calendar.remove_event(*events[0])
        case _:
            return events


def modify(search_term: str, parameters, calendar: calendar.Calendar):
    """
    Update event if search term returns only one result, otherwise return all found events.

    search_term (str): Search term used to find events
    calendar (calendar.Calendar): The calendar in use
    """
    events = calendar.search(search_term)
    match len(events):
        case 1:
            calendar.update_event(*events[0])
        case _:
            return events
    calendar.update_event(*events[0])



def search(search_term: str, calendar: calendar.Calendar):
    events = calendar.search(search_term)
    return events
