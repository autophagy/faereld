# -*- coding: utf-8 -*-

"""
faereld.db
----------
"""

from .models import FaereldEntry
from .graphs import SummaryGraph, BoxPlot
from . import utils

import sqlalchemy
import datetime
import datarum

class FaereldData(object):

    def __init__(self, data_path, config):
        self.session = self._create_session(data_path)
        self.config = config

    def _create_session(self, data_path):
        engine = sqlalchemy.create_engine('sqlite:///{0}'.format(data_path))
        FaereldEntry.metadata.create_all(engine)
        return sqlalchemy.orm.sessionmaker(bind=engine)()

    def get_summary(self, detailed=False):
        entries = self.session.query(FaereldEntry) \
                .order_by(FaereldEntry.start) \
                .all()

        entries_count = len(entries)

        if len(entries) == 0:
            return FaereldEmptySummary()

        total_time = datetime.timedelta(0)
        area_time_map = dict(map(lambda x: (x, []), self.config.get_areas().keys()))
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
                if result.area not in area_time_map:
                    area_time_map[result.area] = [result_time]
                else:
                    area_time_map[result.area].append(result_time)

        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1

        simple_summary = FaereldSimpleSummary(days, entries_count, formatted_time)

        if detailed:
            return FaereldDetailedSummary(simple_summary, area_time_map, last_entries, self.config)
        else:
            return simple_summary

    def get_projects_summary(self):
        entries = self.session.query(FaereldEntry) \
                .filter(FaereldEntry.area.in_(list(self.config.get_project_areas().keys()))) \
                .order_by(FaereldEntry.start) \
                .all()

        entries_count = len(entries)

        if len(entries) == 0:
            return FaereldEmptySummary()

        total_time = datetime.timedelta(0)
        project_time_map = {}

        for index, result in enumerate(entries):
            if index == 0:
                first_day = result.start

            if index == len(entries)-1:
                last_day = result.end

            result_time = result.end - result.start
            total_time += result_time

            if result.object not in project_time_map:
                project_time_map[result.object] = [result_time]
            else:
                project_time_map[result.object].append(result_time)

        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1

        simple_summary = FaereldSimpleSummary(days, entries_count, formatted_time)

        return FaereldProjectsSummary(simple_summary, project_time_map, self.config)

    def get_last_objects(self, area, limit):
        objects = self.session.query(FaereldEntry.object) \
                  .filter(FaereldEntry.area == area) \
                  .distinct(FaereldEntry.object) \
                  .order_by(FaereldEntry.start.desc()) \
                  .limit(limit) \
                  .all()

        return objects

    def create_entry(self, area, object, link, start, end):
        entry = FaereldEntry(area=area,
                             object=object,
                             link=link,
                             start=start,
                             end=end)

        self.session.add(entry)
        self.session.commit()

class FaereldEmptySummary(object):

    def print(self):
        print("No Færeld entries found!")

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

        def __init__(self, simple_summary, area_time_map, last_entries, config):
            self.simple_summary = simple_summary
            self.area_time_map = area_time_map
            self.last_entries = last_entries
            self.config = config

        def print(self):
            self.simple_summary.print()
            print()

            utils.print_header("TOTAL TIME LOGGED PER AREA")
            print()
            graph = SummaryGraph(self.area_time_map, utils.max_width(self.config.get_max_graph_width()), self.config.get_exclude_from_total_time()) \
                    .generate()
            for row in graph:
                print(row)

            print()
            utils.print_header("ENTRY TIME DISTRIBUTION PER AREA")
            print()
            box = BoxPlot(self.area_time_map, utils.max_width(self.config.get_max_graph_width()), self.config.get_exclude_from_entry_time_distribution()) \
                         .generate()
            for row in box:
                print(row)

            print()
            utils.print_header("LAST {0} ENTRIES".format(len(self.last_entries)))
            print()
            for entry in self.last_entries:
                if self.config.get_use_wending():
                    start_date = datarum.from_date(entry.start)
                else:
                    start_date = entry.start

                utils.print_rendered_string(entry.area,
                                            self.config.get_area(entry.area),
                                            start_date,
                                            self.config.get_object_name(entry.area, entry.object),
                                            utils.time_diff(entry.start, entry.end))


class FaereldProjectsSummary(object):

        def __init__(self, simple_summary, project_time_map, config):
            self.simple_summary = simple_summary
            self.project_time_map = project_time_map
            self.config = config

        def print(self):
            self.simple_summary.print()
            print()

            utils.print_header("TOTAL TIME LOGGED PER PROJECT")
            print()
            graph = SummaryGraph(self.project_time_map, utils.max_width(self.config.get_max_graph_width()),
                                 key_transform_func = self.config.get_project_name) \
                    .generate()
            for row in graph:
                print(row)
