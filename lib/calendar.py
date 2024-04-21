from datetime import datetime
from difflib import SequenceMatcher
from lib.event import Event
import lib.parsers


class Calendar():
    def __init__(self, events: list[Event]=[]):
        """
        Initialize the calendar.

        events (list[Event]): List containing events (default empty list)
        """
        self.events = events
    

    def add_event(self, event_new: Event):
        """
        Add event to the calendar

        event_new (Event): Event to be added
        """
        self.events.append(event_new)


    def remove_event(self, index: int, event: Event):
        self.events.pop(index)


    def update_event(self, index: int, event: Event):
        """
        Update an event at given index
        index (int): Index of the target event
        event (Event): Updated event
        """
        self.events[index].update(event)


    def get_by_range(self, date_start: datetime, date_end: datetime):
        """
        Get events in given date range

        date_start (datetime): Start of the range
        date_end (datetime): End of the range
        """
        return [(i, _event) for i, _event in enumerate(self.events)
                if date_start >= _event.start >= date_end]


    def get_by_date(self, date_start: datetime):
        """
        Get events by a spesific full date (yyy/mm/dd)
        
        date_start (datetime): Starting date of the range (one day)
        """
        return [(i, _event) for i, _event in enumerate(self.events)
                if _event.date_start.date == date_start.date]


    def get_by_month(self, date_start: datetime):
        """
        Get events by a spesific month (yyy/mm)
        
        date_start (datetime): Starting date of the range (one month)
        """
        return [(i, _event) for i, _event in enumerate(self.events)
                if _event.date_start.month == date_start.month]


    def get_by_year(self, date_start: datetime):
        """
        Get events by a spesific year (yyy)
        
        date_start (datetime): Starting date of the range (one year)
        """
        return [(i, _event) for i, _event in enumerate(self.events)
                if _event.date_start.year == date_start.year]


    def get_by_title(self, search_string: str):
        """
        Get events based on exact title
        
        search_string (str): Title of the event
        """
        return [(i, _event) for i, _event in enumerate(self.events)
                if search_string == _event.title]


    def get_by_title_substring(self, search_string: str):
        """
        Get events based on partial title
        
        search_string (str): Part of the title of the event
        """
        return [(i, _event) for i, _event in enumerate(self.events)
                if search_string in _event.title]
    

    def get_by_title_fuzzy(self, search_string: str, delta: float=0.5):
        """
        Get events based on fuzzy title
        
        search_string (str): Fuzzy event title
        delta (float, default 0.5): Minimum ratio of difference between the search string and the calendar entry
        """
        return [(i, _event) for i, _event in enumerate(self.events)
                if SequenceMatcher(None, search_string, _event.title).ratio() > delta]


    def get_by_author(self, search_string: str):
        """
        Get events by author

        search_string (str): Author of the events
        """
        return [(i, _event) for i, _event in enumerate(self.events)
                if search_string in _event.author]
    

    def search(self, search_string: str):
        """
        Searches for calendar events based on a search string

        search_string (str): Either a date, a range of dates, (fuzzy) title or the author
        """
        date_start, date_end = lib.parsers.parse_date_range(search_string)

        events = None
        match date_start, date_end:
            case True, True:
                events = self.get_by_range(date_start, date_end)
            case True, False:
                events = self.get_by_date(date_start)
            case False, False:
                events = self.get_by_title(search_string)
                events.append(self.get_by_author(search_string))
                if len(events) == 0:
                    events = self.get_by_title_fuzzy(search_string)
                    events.append(self.get_by_title_substring(search_string))
        
        return set(events)
