# -*- coding: utf-8 -*-
"""
faereld.summaries.productivity
------------------------------

A summary of productivity, measured in time spent per day of the week and
hour of the day.
"""

from faereld.printer import Printer
from faereld.graphs.summary_graph import SummaryGraph
from faereld import utils


class ProductivitySummary(object):

    def __init__(self, simple_summary, hour_delta_map, day_delta_map, config):
        self.simple_summary = simple_summary
        self.hour_delta_map = hour_delta_map
        self.day_delta_map = day_delta_map
        self.config = config

    def print(self):
        self.simple_summary.print()
        p = Printer()

        def day_num_to_string(day_num):
            dates = {
                0: 'MON', 1: 'TUE', 2: 'WED', 3: 'THU', 4: 'FRI', 5: 'SAT', 6: 'SUN'
            }
            return dates[day_num]

        def zero_pad_hour(hour):
            if len(str(hour)) == 1:
                return '0{}'.format(str(hour))

            return str(hour)

        p.newline()
        p.add_header("Total Time Logged Per Day")
        p.newline()
        graph = SummaryGraph(self.day_delta_map).set_max_width(
            utils.max_width(self.config.get_max_graph_width())
        ).set_key_transform_function(
            day_num_to_string
        ).generate()
        for row in graph:
            p.add_nowrap(row)
        p.newline()
        p.add_header("Total time logged per hour")
        p.newline()
        graph = SummaryGraph(self.hour_delta_map).set_max_width(
            utils.max_width(self.config.get_max_graph_width())
        ).set_key_transform_function(
            zero_pad_hour
        ).generate()
        for row in graph:
            p.add_nowrap(row)
        p.print()
