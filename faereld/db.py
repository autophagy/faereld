# -*- coding: utf-8 -*-

"""
faereld.db
----------
"""

from .models import FaereldEntry
from .graph import SummaryGraph, BoxPlot
from . import utils

from os import get_terminal_size
import sqlalchemy
import datetime
import datarum

class FaereldData(object):

    def __init__(self, data_path):
        self.session = self._create_session(data_path)

    def _create_session(self, data_path):
        engine = sqlalchemy.create_engine('sqlite:///{0}'.format(data_path))
        FaereldEntry.metadata.create_all(engine)
        return sqlalchemy.orm.sessionmaker(bind=engine)()

    def get_summary(self, detailed=False):
        entries_count = self.session.query(FaereldEntry).count()

        entries = self.session.query(FaereldEntry) \
                .order_by(FaereldEntry.start) \
                .all()

        total_time = datetime.timedelta(0)
        area_time_map = dict(map(lambda x: (x, []), utils.areas.keys()))
        last_entries = entries[-10:]
        last_entries.reverse()

        for index, result in enumerate(entries):
            if index == 0:
                first_day = result.start

            if index == len(entries)-1:
                last_day = result.end

            result_time = result.end - result.start
            total_time += result_time

            if detailed:
                area_time_map[result.area].append(result_time)

        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1

        simple_summary = FaereldSimpleSummary(days, entries_count, formatted_time)

        if detailed:
            return FaereldDetailedSummary(simple_summary, area_time_map, last_entries)
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
            utils.print_header("{0} DAYS // {1} ENTRIES // TOTAL {2}".format(self.days,
                                                          self.entries,
                                                          self.formatted_time))

class FaereldDetailedSummary(object):

        def __init__(self, simple_summary, area_time_map, last_entries):
            self.simple_summary = simple_summary
            self.area_time_map = area_time_map
            self.last_entries = last_entries

        def print(self):
            self.simple_summary.print()
            print()

            utils.print_header("TOTAL TIME LOGGED PER AREA")
            print()
            graph = SummaryGraph(self.area_time_map,
                                 get_terminal_size().columns) \
                    .generate()
            for row in graph:
                print(row)

            print()
            utils.print_header("ENTRY TIME DISTRIBUTION PER AREA")
            print()
            box = BoxPlot(self.area_time_map,
                          get_terminal_size().columns) \
                         .generate()
            for row in box:
                print(row)

            print()
            utils.print_header("LAST {0} ENTRIES".format(len(self.last_entries)))
            print()
            for entry in self.last_entries:
                utils.print_rendered_string(entry.area, datarum.from_date(entry.start), entry.object, utils.time_diff(entry.start, entry.end))
