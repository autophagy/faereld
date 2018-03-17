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

from faereld.printer import Printer
from faereld.graphs.summary_graph import SummaryGraph
from faereld.graphs.box_plot import BoxPlot
from faereld import utils
import datetime


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
        graph = SummaryGraph(summary_time_map).set_max_width(
            utils.max_width(self.config.get_max_graph_width())
        ).set_exclude_list(
            self.config.get_exclude_from_total_time()
        ).generate()
        for row in graph:
            p.add_nowrap(row)
        p.newline()
        p.add_header("ENTRY TIME DISTRIBUTION PER AREA")
        p.newline()
        box = BoxPlot(self.area_time_map).set_max_width(
            utils.max_width(self.config.get_max_graph_width())
        ).set_exclude_list(
            self.config.get_exclude_from_entry_time_distribution()
        ).generate()
        for row in box:
            p.add_nowrap(row)
        p.newline()
        p.add_header("LAST {0} ENTRIES".format(len(self.last_entries)))
        p.newline()
        for entry in self.last_entries:
            if self.config.get_use_wending():
                start_date = entry['START'].strftime('{daeg} {month} {gere}')
            else:
                start_date = entry['START'].strftime('%d %b %Y')
            p.add(
                *utils.get_rendered_string(
                    entry['AREA'],
                    self.config.get_area(entry['AREA']),
                    start_date,
                    self.config.get_object_name(entry['AREA'], entry['OBJECT']),
                    utils.time_diff(entry['START'], entry['END']),
                )
            )
        p.print()
