# -*- coding: utf-8 -*-

"""
faereld.graphs.summary_graph
-----------
"""

from .. import utils
from datetime import timedelta

class SummaryGraph(object):

    bar_character = '━'
    label_seperator = '  '

    def __init__(self, values_map):
        self.values_map = values_map
        self.max_width = utils.terminal_width()
        self.exclude_list = []
        self.key_transform_func = None
        self.sort = False

    def set_max_width(self, max_width):
        self.max_width = max_width
        return self

    def set_exclude_list(self, exclude_list):
        self.exclude_list = exclude_list
        return self

    def set_key_transform_function(self, key_transform_func):
        self.key_transform_func = key_transform_func
        return self

    def sort_graph(self, reverse=False):
        self.sort = True
        self.reverse_sort = reverse
        return self

    def generate(self):

        # Filter out areas that are invalid for this analysis
        values = dict(filter(lambda x: x[0] not in self.exclude_list, self.values_map.items()))

        # Total up the values
        area_total_dict = dict(map(lambda x: (x[0], sum(x[1], timedelta())), values.items()))

        # First, create the graph labels
        if self.key_transform_func is not None:
            # If a key transform func is given, then transform the keys
            area_total_dict = dict(map(lambda x: (self.key_transform_func(x[0]), x[1]), area_total_dict.items()))

        longest_key = max(len(key) for key in area_total_dict.keys())
        labels = dict(map(lambda x: (x[0], '{0} [{1}]'.format(self._pad_key(x[0], longest_key), utils.format_time_delta(x[1]))), area_total_dict.items()))

        # Get the length of the longest label
        longest_label = len(max(labels.values(), key=len))

        for k, v in labels.items():
            if len(v) < longest_label:
                labels[k] = v + ' '*(longest_label-len(v)) + self.label_seperator
            else:
                labels[k] = v + self.label_seperator

        # Update the max width with the longest label
        self.max_width -= longest_label + len(self.label_seperator)

        # Convert the timedeltas into percentages
        largest_delta = max(area_total_dict.values())

        percentages = dict(map(lambda x: (x[0], x[1]/largest_delta), area_total_dict.items()))

        # Create the bars based on the percentages and max max_width

        bars = dict(map(lambda x: (x[0], round(self.max_width*x[1]) * self.bar_character), percentages.items()))

        # Sort, if needed

        if self.sort:
            graph_keys = sorted(bars, key=bars.get, reverse=self.reverse_sort)
        else:
            graph_keys = list(bars.keys())

        return list(map(lambda t: "{0}{1}".format(labels[t], bars[t]), graph_keys))

    def _pad_key(self, key, length):
        if len(key) < length:
            return key + ' '*(length - len(key))
        else:
            return key
