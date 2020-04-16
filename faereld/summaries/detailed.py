# -*- coding: utf-8 -*-
"""
faereld.summaries.detailed
--------------------------

A summary to display detailed general information about the tasks tracked
in Faereld. So far:

TOTAL TIME LOGGED PER AREA       :: Aggregation of time spent over all areas
ENTRY TIME DISTRIBUTION PER AREA :: Distribution of time spent over all areas
LAST 10 ENTRIES                  :: The last 10 entries logged
"""

import datetime

from faereld import utils
from faereld.graphs import BoxPlot, SummaryGraph
from faereld.printer import Printer


class DetailedSummary(object):
    def __init__(self, simple_summary, area_time_map, last_entries, config):
        self.simple_summary = simple_summary
        self.area_time_map = area_time_map
        self.last_entries = last_entries
        self.config = config

    def print(self):
        self.simple_summary.print()
        p = Printer()
        p.newline()
        p.add_header("Total Time Logged Per Area")
        p.newline()
        # Sum all the timedeltas for the summary graph
        summary_time_map = dict(
            map(
                lambda x: (x[0], sum(x[1], datetime.timedelta())),
                self.area_time_map.items(),
            )
        )
        graph = (
            SummaryGraph(summary_time_map)
            .set_max_width(utils.max_width(self.config.max_graph_width))
            .set_exclude_list(self.config.exclude_from_total_time)
            .generate()
        )
        for row in graph:
            p.add_nowrap(row)
        p.newline()
        p.add_header("ENTRY TIME DISTRIBUTION PER AREA")
        p.newline()
        box = (
            BoxPlot(self.area_time_map)
            .set_max_width(utils.max_width(self.config.max_graph_width))
            .set_exclude_list(self.config.exclude_from_entry_time_distribution)
            .generate()
        )
        for row in box:
            p.add_nowrap(row)
        p.newline()
        p.add_header("LAST {0} ENTRIES".format(len(self.last_entries)))
        p.newline()
        for entry in self.last_entries:
            if self.config.use_wending:
                start_date = entry.start.strftime("{daeg} {month} {gere}")
            else:
                start_date = entry.start.strftime("%d %b %Y")
            p.add(
                *utils.get_rendered_string(
                    entry.area,
                    self.config.get_area(entry.area),
                    start_date,
                    self.config.get_object_name(entry.area, entry.obj),
                    utils.time_diff(entry.start, entry.end),
                    entry.start,
                    entry.end,
                    entry.purpose,
                )
            )
        p.print()


class DetailedAreaSummary(object):
    def __init__(self, simple_summary, area, area_time_map, last_entries, config):
        self.simple_summary = simple_summary
        self.area_time_map = area_time_map
        self.last_entries = last_entries
        self.config = config
        self.area = area
        self.area_name = config.get_area(area)["name"]

    def print(self):
        self.simple_summary.print()
        p = Printer()
        p.newline()
        p.add_header(f"Summary For {self.area_name}")
        p.newline()

        minimum = None
        maximum = None
        average = datetime.timedelta()

        for entry in self.area_time_map[self.area]:
            if minimum is None or minimum > entry:
                minimum = entry
            if maximum is None or maximum < entry:
                maximum = entry
            average += entry

        average = average / len(self.area_time_map[self.area])

        p.add(
            f"The lowest recorded entry for {self.area_name} is ",
            f"{utils.format_time_delta(minimum)}.",
        )
        p.add(
            f"The highest recorded entry for {self.area_name} is ",
            f"{utils.format_time_delta(maximum)}.",
        )
        p.add(
            f"The average entry for {self.area_name} is ",
            f"{utils.format_time_delta(average)}.",
        )

        p.newline()
        p.add_header(f"Entry Time Distribution for {self.area_name}")
        p.newline()
        box = (
            BoxPlot(self.area_time_map)
            .set_max_width(utils.max_width(self.config.max_graph_width))
            .set_exclude_list(self.config.exclude_from_entry_time_distribution)
            .generate()
        )
        for row in box:
            p.add_nowrap(row)
        p.newline()
        p.add_header("LAST {0} ENTRIES".format(len(self.last_entries)))
        p.newline()
        for entry in self.last_entries:
            if self.config.use_wending:
                start_date = entry.start.strftime("{daeg} {month} {gere}")
            else:
                start_date = entry.start.strftime("%d %b %Y")
            p.add(
                *utils.get_rendered_string(
                    entry.area,
                    self.config.get_area(entry.area),
                    start_date,
                    self.config.get_object_name(entry.area, entry.obj),
                    utils.time_diff(entry.start, entry.end),
                    entry.purpose,
                )
            )
        p.print()
