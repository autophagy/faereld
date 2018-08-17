# -*- coding: utf-8 -*-
"""
faereld.db
----------
"""

from faereld.models import FaereldWendingEntry, FaereldDatetimeEntry
from faereld.summaries.simple import SimpleSummary
from faereld.summaries.empty import EmptySummary
from faereld.summaries.detailed import DetailedSummary, DetailedAreaSummary
from faereld.summaries.projects import ProjectsSummary
from faereld.summaries.productivity import ProductivitySummary
from faereld import utils

from os import path

import wisdomhord
from datetime import timedelta


class FaereldData(object):
    def __init__(self, data_path, config):
        self.config = config
        self.hord = self._create_session(data_path)

    def _create_session(self, data_path):
        hord_path = path.expanduser(data_path)
        if self.config.get_use_wending():
            self.bisen = FaereldWendingEntry
        else:
            self.bisen = FaereldDatetimeEntry
        if not path.exists(hord_path):
            # Init the hord
            return wisdomhord.cennan(hord_path, bisen=self.bisen)

        else:
            return wisdomhord.hladan(hord_path, bisen=self.bisen)

    def get_summary(self, target=None, detailed=False):
        if target is None:
            entries = self.hord.get_rows()
        else:
            entries = self.hord.get_rows(filter_func=lambda x: x.area == target)
        entries_count = len(entries)
        if len(entries) == 0:
            return EmptySummary()

        total_time = timedelta(0)
        area_time_map = dict(map(lambda x: (x, []), self.config.get_areas().keys()))
        last_entries = entries[:10]
        first_day = None
        last_day = None
        for result in entries:
            if first_day is None or result.start < first_day:
                first_day = result.start
            if last_day is None or result.end > last_day:
                last_day = result.end
            result_time = result.end - result.start
            total_time += result_time
            if detailed:
                area_time_map[result.area].append(result_time)
        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1
        simple_summary = SimpleSummary(days, entries_count, formatted_time)
        if detailed and target is not None:
            return DetailedAreaSummary(
                simple_summary, target, area_time_map, last_entries, self.config
            )
        elif detailed:
            return DetailedSummary(
                simple_summary, area_time_map, last_entries, self.config
            )

        else:
            return simple_summary

    def get_projects_summary(self):
        def projects_filter(entry):
            return entry.area in list(self.config.get_project_areas().keys())

        entries = self.hord.get_rows(filter_func=projects_filter)
        entries_count = len(entries)
        if len(entries) == 0:
            return EmptySummary()

        total_time = timedelta(0)
        project_time_map = {}
        project_area_time_map = {}
        first_day = None
        last_day = None
        for result in entries:
            if first_day is None or result.start < first_day:
                first_day = result.start
            if last_day is None or result.end > last_day:
                last_day = result.end
            result_time = result.end - result.start
            total_time += result_time
            if result.obj not in project_time_map:
                project_time_map[result.obj] = result_time
            else:
                project_time_map[result.obj] += result_time
            if result.obj not in project_area_time_map:
                empty_map = dict(
                    map(
                        lambda x: (x, timedelta(0)),
                        self.config.get_project_areas().keys(),
                    )
                )
                project_area_time_map[result.obj] = empty_map
                project_area_time_map[result.obj][result.area] += result_time
            else:
                if result.area not in project_area_time_map[result.obj]:
                    project_area_time_map[result.obj][result.area] = result_time
                else:
                    project_area_time_map[result.obj][result.area] += result_time
        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1
        simple_summary = SimpleSummary(days, entries_count, formatted_time)
        return ProjectsSummary(
            simple_summary, project_time_map, project_area_time_map, self.config
        )

    def get_productivity_summary(self):
        def determine_dominant_hour(start_time, end_time):
            half_delta = (end_time - start_time) / 2
            if (start_time + half_delta).hour == start_time.hour:
                return start_time.hour

            else:
                return end_time.hour

        entries = self.hord.get_rows()
        entries_count = len(entries)
        if len(entries) == 0:
            return EmptySummary()

        total_time = timedelta(0)
        hour_delta_map = {k: timedelta(0) for k in list(range(0, 24))}
        day_delta_map = {k: timedelta(0) for k in list(range(0, 7))}
        first_day = None
        last_day = None
        for result in entries:
            if first_day is None or result.start < first_day:
                first_day = result.start
            if last_day is None or result.end > last_day:
                last_day = result.end
            result_time = result.end - result.start
            total_time += result_time
            hour = determine_dominant_hour(result.start, result.end)
            hour_delta_map[hour] += result.end - result.start
            day_delta_map[result.start.weekday()] += result.end - result.start
        formatted_time = utils.format_time_delta(total_time)
        days = (last_day - first_day).days + 1
        simple_summary = SimpleSummary(days, entries_count, formatted_time)
        return ProductivitySummary(
            simple_summary, hour_delta_map, day_delta_map, self.config
        )

    def get_last_objects(self, area, limit):
        objects = self.hord.get_rows(
            filter_func=lambda x: x.area == area,
            sort_by=self.bisen.start,
            reverse_sort=True,
        )
        filtered_obj = []
        for obj in objects:
            if obj.obj not in filtered_obj:
                filtered_obj.append(obj.obj)
        return filtered_obj[:limit]

    def create_entry(self, entry):
        if self.config.get_use_wending():
            bisen = FaereldWendingEntry
        else:
            bisen = FaereldDatetimeEntry
        insert_entry = bisen(
            area=entry["AREA"],
            obj=entry["OBJECT"],
            start=entry["START"],
            end=entry["END"],
        )

        self.hord.insert(insert_entry)
