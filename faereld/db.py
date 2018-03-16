# -*- coding: utf-8 -*-

"""
faereld.db
----------
"""

from .models import FaereldWendingEntry, FaereldDatetimeEntry
from .graphs import SummaryGraph, BoxPlot, SummaryMultiGraph
from .summaries import SimpleSummary, EmptySummary, DetailedSummary, ProjectsSummary, ProductivitySummary
from . import utils
from .printer import Printer

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
            return wisdomhord.cennan(hord_path, bisen=bisen)
        else:
            return wisdomhord.hladan(hord_path, bisen=bisen)

    def get_summary(self, detailed=False):
        entries = self.hord.get_rows()

        entries_count = len(entries)

        if len(entries) == 0:
            return EmptySummary()

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

        simple_summary = SimpleSummary(days, entries_count, formatted_time)

        if detailed:
            return DetailedSummary(simple_summary, area_time_map, last_entries, self.config)
        else:
            return simple_summary

    def get_projects_summary(self):
        projects_filter = lambda x: x['AREA'] in list(self.config.get_project_areas().keys())
        entries = self.hord.get_rows(filter_func=projects_filter)

        entries_count = len(entries)

        if len(entries) == 0:
            return EmptySummary()

        total_time = datetime.timedelta(0)
        project_time_map = {}
        project_area_time_map = {}


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

            if result['OBJECT'] not in project_area_time_map:
                    empty_map = dict(map(lambda x: (x, datetime.timedelta(0)),
                                    self.config.get_project_areas().keys()))
                    project_area_time_map[result['OBJECT']] = empty_map
                    project_area_time_map[result['OBJECT']][result['AREA']] += result_time
            else:
                if result['AREA'] not in project_area_time_map[result['OBJECT']]:
                    project_area_time_map[result['OBJECT']][result['AREA']] = result_time
                else:
                    project_area_time_map[result['OBJECT']][result['AREA']] += result_time

        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1

        simple_summary = SimpleSummary(days, entries_count, formatted_time)

        return ProjectsSummary(simple_summary,
                                      project_time_map,
                                      project_area_time_map,
                                      self.config)

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
            return EmptySummary()

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

        simple_summary = SimpleSummary(days, entries_count, formatted_time)

        return ProductivitySummary(simple_summary, hour_delta_map, day_delta_map, self.config)


    def get_last_objects(self, area, limit):
        objects = self.hord.get_rows(filter_func=lambda x: x['AREA'] == area,
            sort_by='START', reverse_sort=True)

        filtered_obj = []

        for obj in objects:
            if obj['OBJECT'] not in filtered_obj:
                filtered_obj.append(obj['OBJECT'])

        return filtered_obj[:limit]

    def create_entry(self, entry):
        self.hord.insert(entry)
