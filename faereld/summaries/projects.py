# -*- coding: utf-8 -*-
"""
faereld.summaries.projects
--------------------------

A summary of time spent across all project specific tasks. Currently::

TOTAL TIME LOGGED PER PROJECT :: Aggregation of time spent on each project
TOTAL TIME LOGGED PER AREA    :: Aggregation of time spent on individual areas
                                 within a project.
"""

from faereld.graphs.summary_graph import SummaryGraph
from faereld.graphs.summary_multigraph import SummaryMultiGraph
from faereld.printer import Printer

from .. import utils


class ProjectsSummary(object):
    def __init__(self, simple_summary, project_time_map, project_area_time_map, config):
        self.simple_summary = simple_summary
        self.project_time_map = project_time_map
        self.project_area_time_map = project_area_time_map
        self.config = config

    def print(self):
        self.simple_summary.print()
        p = Printer()
        p.newline()
        p.add_header("Total Time Logged Per Project")
        p.newline()
        graph = (
            SummaryGraph(self.project_time_map)
            .set_max_width(utils.max_width(self.config.get_max_graph_width()))
            .set_key_transform_function(self.config.get_project_name)
            .sort_graph(reverse=True)
            .generate()
        )
        for row in graph:
            p.add_nowrap(row)
        p.newline()
        p.add_header("Total Time Logged Per Area Per Project")
        p.newline()
        multigraph = (
            SummaryMultiGraph(self.project_area_time_map, 30)
            .set_header_transform_function(self.config.get_project_name)
            .generate()
        )
        for row in multigraph:
            p.add_nowrap(row)
        p.print()
