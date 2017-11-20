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

    def get_summary(self):
        entries = self.session.query(FaereldEntry).count()

        days = self.session.query(FaereldEntry.area,
                                  FaereldEntry.start,
                                  FaereldEntry.end) \
                .order_by(FaereldEntry.start) \
                .all()

        total_time = datetime.timedelta(0)
        area_time_map = dict(map(lambda x: (x, datetime.timedelta(0)),
                                 utils.areas.keys()))

        for index, result in enumerate(days):
            if index == 0:
                first_day = result[1]

            if index == len(days)-1:
                last_day = result[2]

            total_time += result[2] - result[1]
            area_time_map[result[0]] += result[2] - result[1]

        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1
        return FaereldSummary(days, entries, formatted_time, area_time_map)

    def create_entry(self, area, object, link, start, end):
        entry = FaereldEntry(area=area,
                             object=object,
                             link=link,
                             start=start,
                             end=end)

        self.session.add(entry)
        self.session.commit()

class FaereldSummary(object):

        def __init__(self, days, entries, formatted_time, area_time_map):
            self.days = days
            self.entries = entries
            self.formatted_time = formatted_time
            self.area_time_map = area_time_map

        def print_short_summary(self):
            print("{0} Days // {1} Entries // {2}".format(self.days,
                                                          self.entries,
                                                          self.formatted_time))

        def print_detailed_summary(self):
            graph = SummaryGraph().generate(self.area_time_map,
                                            get_terminal_size().columns)

            for row in graph:
                print(row)


