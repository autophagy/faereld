# -*- coding: utf-8 -*-

"""
faereld.db
----------
"""

from .models import FaereldWendingEntry, FaereldDatetimeEntry
from .graphs import SummaryGraph, BoxPlot
from . import utils

from os import path

import wisdomhord
import datetime
import datarum

class FaereldData(object):

    def __init__(self, data_path, config):
        self.config = config
        self.hord = self._create_session(data_path)

    def _create_session(self, data_path):
        hord_path = path.expanduser(data_path)
        if self.config.get_use_wending():
            bisen = FaereldWendingEntry
        else:
            bisen = FaereldDatetimeEntry
        if not path.exists(hord_path):
            # Init the hord
            return wisdomhord.cenann(hord_path, bisen=bisen)
        else:
            return wisdomhord.hladan(hord_path, bisen=bisen)

    def get_summary(self, detailed=False):
        entries = self.hord.get_rows()

        entries_count = len(entries)

        if len(entries) == 0:
            return FaereldEmptySummary()

        total_time = datetime.timedelta(0)
        area_time_map = dict(map(lambda x: (x, []), self.config.get_areas().keys()))
        last_entries = entries[:10]

        first_day = None
        last_day = None

        for index, result in enumerate(entries):
            if first_day == None:
                first_day = result['START']
                last_day = result['START']

            if result['START'] < first_day:
                first_day = result['START']
            elif result['START'] > last_day:
                last_day = result['START']

            result_time = result['END'] - result['START']
            total_time += result_time

            if detailed:
                area_time_map[result['AREA']].append(result_time)

        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1

        simple_summary = FaereldSimpleSummary(days, entries_count, formatted_time)

        if detailed:
            return FaereldDetailedSummary(simple_summary, area_time_map, last_entries, self.config)
        else:
            return simple_summary

    def get_projects_summary(self):
        projects_filter = lambda x: x['AREA'] in list(self.config.get_project_areas().keys())
        entries = self.hord.get_rows(filter_func=projects_filter)

        entries_count = len(entries)

        if len(entries) == 0:
            return FaereldEmptySummary()

        total_time = datetime.timedelta(0)
        project_time_map = {}


        first_day = None
        last_day = None

        for index, result in enumerate(entries):
            if first_day == None:
                first_day = result['START']
                last_day = result['START']

            if result['START'] < first_day:
                first_day = result['START']
            elif result['START'] > last_day:
                last_day = result['START']

            result_time = result['END'] - result['START']
            total_time += result_time

            if result['OBJECT'] not in project_time_map:
                project_time_map[result['OBJECT']] = result_time
            else:
                project_time_map[result['OBJECT']] += result_time

        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1

        simple_summary = FaereldSimpleSummary(days, entries_count, formatted_time)

        return FaereldProjectsSummary(simple_summary, project_time_map, self.config)

    def get_productivity_summary(self):
        def determine_dominant_hour(start_time, end_time):
            half_delta = (end_time - start_time)/2
            if (start_time + half_delta).hour == start_time.hour:
                return start_time.hour
            else:
                return end_time.hour

        entries = self.hord.get_rows()

        entries_count = len(entries)

        if len(entries) == 0:
            return FaereldEmptySummary()

        total_time = datetime.timedelta(0)
        hour_delta_map = {k: datetime.timedelta(0) for k in list(range(0,24))}
        day_delta_map = {k: datetime.timedelta(0) for k in list(range(0,7))}

        first_day = None
        last_day = None

        for index, result in enumerate(entries):
            if first_day == None:
                first_day = result['START']
                last_day = result['START']

            if result['START'] < first_day:
                first_day = result['START']
            elif result['START'] > last_day:
                last_day = result['START']

            result_time = result['END'] - result['START']
            total_time += result_time

            hour = determine_dominant_hour(result['START'], result['END'])
            hour_delta_map[hour] += result['END'] - result['START']
            day_delta_map[result['START'].weekday()] += result['END'] - result['START']

        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1

        simple_summary = FaereldSimpleSummary(days, entries_count, formatted_time)

        return FaereldProductivitySummary(simple_summary, hour_delta_map, day_delta_map, self.config)


    def get_last_objects(self, area, limit):
        objects = self.hord.get_rows(filter_func=lambda x: x['AREA'] == area,
            sort_by='START', reverse_sort=True)

        filtered_obj = []

        for obj in objects:
            if obj['OBJECT'] not in filtered_obj:
                filtered_obj.append(obj['OBJECT'])

        return filtered_obj[:limit]

    def create_entry(self, area, object, link, start, end):
        entry = {
            'AREA': area,
            'OBJECT': object,
            'START': start,
            'END': end,
        }

        self.hord.insert(entry)

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

            # Sum all the timedeltas for the summary graph
            summary_time_map = dict(map(lambda x: (x[0], sum(x[1], datetime.timedelta())),
                                        self.area_time_map.items()))

            graph = SummaryGraph(summary_time_map) \
                  .set_max_width(utils.max_width(self.config.get_max_graph_width())) \
                  .set_exclude_list(self.config.get_exclude_from_total_time()) \
                  .generate()

            for row in graph:
                print(row)

            print()
            utils.print_header("ENTRY TIME DISTRIBUTION PER AREA")
            print()
            box = BoxPlot(self.area_time_map) \
                .set_max_width(utils.max_width(self.config.get_max_graph_width())) \
                .set_exclude_list(self.config.get_exclude_from_entry_time_distribution()) \
                .generate()
            for row in box:
                print(row)

            print()
            utils.print_header("LAST {0} ENTRIES".format(len(self.last_entries)))
            print()
            for entry in self.last_entries:
                if self.config.get_use_wending():
                    start_date = entry['START'].strftime('{daeg} {month} {gere}')
                else:
                    start_date = entry['START'].strftime('%d %b %Y')

                utils.print_rendered_string(entry['AREA'],
                                            self.config.get_area(entry['AREA']),
                                            start_date,
                                            self.config.get_object_name(entry['AREA'], entry['OBJECT']),
                                            utils.time_diff(entry['START'], entry['END']))


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
            graph = SummaryGraph(self.project_time_map) \
                  .set_max_width(utils.max_width(self.config.get_max_graph_width())) \
                  .set_key_transform_function(self.config.get_project_name) \
                  .sort_graph(reverse=True) \
                  .generate()
            for row in graph:
                print(row)


class FaereldProductivitySummary(object):

        def __init__(self, simple_summary, hour_delta_map, day_delta_map, config):
            self.simple_summary = simple_summary
            self.hour_delta_map = hour_delta_map
            self.day_delta_map = day_delta_map
            self.config = config

        def print(self):
            self.simple_summary.print()

            def day_num_to_string(day_num):
                dates = {0: 'MON',
                         1: 'TUE',
                         2: 'WED',
                         3: 'THU',
                         4: 'FRI',
                         5: 'SAT',
                         6: 'SUN'}
                return dates[day_num]

            print()
            utils.print_header("total time logged per day")
            print()
            graph = SummaryGraph(self.day_delta_map) \
                  .set_max_width(utils.max_width(self.config.get_max_graph_width())) \
                  .set_key_transform_function(day_num_to_string) \
                  .generate()
            for row in graph:
                print(row)

            print()
            utils.print_header("Total time logged per hour")
            print()
            graph = SummaryGraph(self.hour_delta_map) \
                  .set_max_width(utils.max_width(self.config.get_max_graph_width())) \
                  .set_key_transform_function(str) \
                  .generate()
            for row in graph:
                print(row)

