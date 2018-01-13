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

    def __init__(self, area_values_map, max_width, exclude_list=[]):
        self.area_values_map = area_values_map
        self.max_width = max_width
        self.exclude_list = exclude_list

    def generate(self):

        # Filter out areas that are invalid for this analysis
        area_values = dict(filter(lambda x: x[0] not in self.exclude_list, self.area_values_map.items()))

        # Total up the values
        area_total_dict = dict(map(lambda x: (x[0], sum(x[1], timedelta())), area_values.items()))

        # First, create the graph labels
        longest_key = len(max(list(area_total_dict.keys())))
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

        # Merge the labels and bars

        return list(map(lambda t: "{0}{1}".format(t[1], bars[t[0]]), labels.items()))

    def _pad_key(self, key, length):
        if len(key) < length:
            return key + ' '*(length - len(key))
        else:
            return key
