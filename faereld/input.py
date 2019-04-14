import datetime
import time

import datarum
from faereld import utils
from faereld.printer import Printer
from prompt_toolkit import prompt


class Input:
    def __init__(self, name):
        self.name = name

    def gather(self):
        Printer().newline().add_header(self.name).newline().print()
        return prompt(f"{self.name} :: ", vi_mode=True)


class DurationInput:
    def __init__(self, name, use_wending=False):
        self.name = name
        self.use_wending = use_wending

    def gather(self):
        Printer().newline().add_header(self.name).newline().print()
        from_date, to_date = None, None
        while from_date is None and to_date is None:
            while from_date is None:
                from_input = prompt("From :: ", vi_mode=True)
                from_date = self._convert_input_date(from_input)
            while to_date is None:
                to_input = prompt("To :: ", vi_mode=True)
                to_date = self._convert_input_date(to_input)
            if from_date >= to_date:
                print(f"Invalid Duration :: {utils.time_diff(from_date, to_date)}")
                from_date, to_date = None, None
        return from_date, to_date

    def _convert_input_date(self, date_string):
        if self.use_wending:
            return self._parse_date(
                date_string=date_string,
                dt=datarum.wending,
                datetime_format="{daeg} {month} {gere} // {tid_zero}.{minute_zero}",
                example_time="16.15",
                example_datetime="13 Forst 226 // 16.15",
            )
        else:
            return self._parse_date(
                date_string=date_string,
                dt=datetime.datetime,
                datetime_format="%d %b %Y // %H.%M",
                example_time="16.15",
                example_datetime="3 Dec 2018 // 16.15",
            )

    @staticmethod
    def _parse_date(date_string, dt, datetime_format, example_time, example_datetime):
        try:
            if date_string.lower() == "now":
                return dt.now().replace(second=0)
            elif "//" not in date_string:
                parsed_time = time.strptime(date_string, "%H.%M")
                return dt.now().replace(
                    hour=parsed_time.tm_hour, minute=parsed_time.tm_min, second=0
                )
            else:
                return dt.strptime(date_string, datetime_format)
        except (ValueError, TypeError):
            print()
            print(
                f"{date_string} is an invalid date string. For example, it must be of"
                f" the form: '{example_datetime}', '{example_time}' or just 'now'."
            )
            return None
