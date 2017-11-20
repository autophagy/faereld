# -*- coding: utf-8 -*-

"""
faereld.db
----------
"""

from .models import FaereldEntry
from .graph import SummaryGraph
from . import utils

from os import get_terminal_size
import sqlalchemy
import datetime

class FaereldData(object):

    def __init__(self, data_path):
        self.session = self._create_session(data_path)

    def _create_session(self, data_path):
        engine = sqlalchemy.create_engine('sqlite:///{0}'.format(data_path))
        FaereldEntry.metadata.create_all(engine)
        return sqlalchemy.orm.sessionmaker(bind=engine)()

    def get_summary(self, detailed=False):
        entries_count = self.session.query(FaereldEntry).count()

        entries = self.session.query(FaereldEntry.area,
                                  FaereldEntry.start,
                                  FaereldEntry.end) \
                .order_by(FaereldEntry.start) \
                .all()

        total_time = datetime.timedelta(0)
        area_time_map = dict(map(lambda x: (x, datetime.timedelta(0)),
                                 utils.areas.keys()))
        min_time = None
        max_time = None

        for index, result in enumerate(entries):
            if index == 0:
                first_day = result[1]

            if index == len(entries)-1:
                last_day = result[2]

            result_time = result[2] - result[1]
            total_time += result_time

            if detailed:
                if min_time is None or max_time is None:
                    min_time = result_time
                    max_time = result_time

                if result_time < min_time:
                    min_time = result_time
                elif result_time > max_time:
                    max_time = result_time

                area_time_map[result[0]] += result_time


        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1

        simple_summary = FaereldSimpleSummary(days, entries_count, formatted_time)

        if detailed:
            avg_time = utils.format_time_delta(total_time/len(entries))
            min_time = utils.format_time_delta(min_time)
            max_time = utils.format_time_delta(max_time)
            return FaereldDetailedSummary(simple_summary, area_time_map, min_time, max_time, avg_time)
        else:
            return simple_summary

    def create_entry(self, area, object, link, start, end):
        entry = FaereldEntry(area=area,
                             object=object,
                             link=link,
                             start=start,
                             end=end)

        self.session.add(entry)
        self.session.commit()

class FaereldSimpleSummary(object):

        def __init__(self, days, entries, formatted_time):
            self.days = days
            self.entries = entries
            self.formatted_time = formatted_time

        def print(self):
            print("{0} DAYS // {1} ENTRIES // TOTAL {2}".format(self.days,
                                                          self.entries,
                                                          self.formatted_time))

class FaereldDetailedSummary(object):

        def __init__(self, simple_summary, area_time_map, min_time, max_time, avg_time):
            self.simple_summary = simple_summary
            self.area_time_map = area_time_map
            self.min_time = min_time
            self.max_time = max_time
            self.avg_time = avg_time

        def print(self):
            self.simple_summary.print()
            print()
            graph = SummaryGraph().generate(self.area_time_map,
                                            get_terminal_size().columns)
            for row in graph:
                print(row)

            print()
            print("MIN {0} // MAX {1} // AVG {2}".format(self.min_time, self.max_time, self.avg_time))