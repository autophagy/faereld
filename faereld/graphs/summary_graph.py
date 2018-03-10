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
        self.graph_header = None

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

    def set_graph_header(self, graph_header):
        self.graph_header = graph_header
        return self

    def generate(self):

        def compose_row(label, bar):
            num_spaces = self.max_width - (len(label) + len(bar))
            return "{0}{1}{2}".format(label, bar, ' '*num_spaces)

        # Filter out areas that are invalid for this analysis
        values = dict(filter(lambda x: x[0] not in self.exclude_list, self.values_map.items()))

        # First, create the graph labels
        if self.key_transform_func is not None:
            # If a key transform func is given, then transform the keys
            values = dict(map(lambda x: (self.key_transform_func(x[0]), x[1]), values.items()))

        longest_key = max(len(key) for key in values.keys())
        labels = dict(map(lambda x: (x[0], '{0} [{1}]'.format(self._pad_key(x[0], longest_key), self._format_time_delta(x[1]))), values.items()))

        # Get the length of the longest label
        longest_label = len(max(labels.values(), key=len))

        for k, v in labels.items():
            if len(v) < longest_label:
                labels[k] = v + ' '*(longest_label-len(v)) + self.label_seperator
            else:
                labels[k] = v + self.label_seperator

        max_bar_width = self.max_width - (longest_label + len(self.label_seperator))

        # Convert the timedeltas into percentages
        largest_delta = max(values.values())

        percentages = dict(map(lambda x: (x[0], x[1]/largest_delta), values.items()))

        # Create the bars based on the percentages and max max_width

        bars = dict(map(lambda x: (x[0], round(max_bar_width*x[1]) * self.bar_character), percentages.items()))

        # Sort, if needed

        if self.sort:
            graph_keys = sorted(values, key=values.get, reverse=self.reverse_sort)
        else:
            graph_keys = list(bars.keys())

        graph_rows= list(map(lambda t: compose_row(labels[t], bars[t]),
                             graph_keys))

        if self.graph_header:
            trimmed_header = self.graph_header[:self.max_width - 1]
            header_format = "\033[91m{0} {1}\033[0m"
            graph_rows.insert(0, '')
            graph_rows.insert(0, header_format.format(trimmed_header,
                                                 '─'*(self.max_width - 1 - len(trimmed_header))))

        return graph_rows

    def _format_time_delta(self, delta):
        formatted = utils.format_time_delta(delta)
        if formatted == "0h0m":
            return "·"
        return formatted

    def _pad_key(self, key, length):
        if len(key) < length:
            return key + ' '*(length - len(key))
        else:
            return key
