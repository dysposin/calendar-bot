import json
from datetime import datetime
from typing import Self

class Event():
    def __init__(self, 
                 author: str,
                 title: str, 
                 date_start: datetime=None, 
                 date_end: datetime=None, 
                 info: str=None,
                 show_time: bool=False): 
        """
        Contains event information

        author (str): who created the event (required)
        title (str): title of the event (required)
        date_start (datetime): Starting date and time of the event
        date_end (datetime): Ending date and time of the event
        info (str): additional information about the event
        show_time (bool): show the time of the event
        """
        self.author = author
        self.title = title
        self.info = info[:1312]
        self.date_start = date_start
        self.date_end = date_end
        self.show_time = show_time
        self.same_day = date_start.date == date_end.date


    def __str__(self):
        match (self.show_time, self.same_day):
            case (True, True):
                date_start = self.date_start.strftime('%d.%m.%Y %H:%M')
                date_end = self.date_end.strftime('%H:%M')
            case (True, False):
                date_start = self.date_start.strftime('%d.%m.%Y %H:%M')
                date_end = self.date_end.strftime('%d.%m.%Y %H:%M')
            case (False, True):
                date_start = self.date_start.strftime('%d.%m.%Y')
                date_end = None
            case (False, False):
                date_start = self.date_start.strftime('%d.%m.%Y')
                date_end = self.date_end.strftime('%d.%m.%Y')

        date_string = date_start
        if date_end is not None:
            date_string = f"{date_start}-{date_end}"
        response = f"({date_string}) {self.author} {self.title}"
        if self.info is not None:
            response += f"\n{self.info}"
        return response


    def update(self, event: Self):
        """
        Updates self with the values of event
        event (Event): Updated values for the event
        """
        for name, attribute in event.__dict__.items():
            if attribute is not None:
                setattr(self, name)


    def get_json(self):
        """
        Returns the event as a JSON string
        """
        event = {}
        for name, attribute in self.__dict__.items():
            event[name] = attribute
        return json.dumps(event)

