# -*- coding: utf-8 -*-

"""
faereld.cli
-----------
"""

from . import controller as c

class SummaryGraph(object):

    bar_character = '/'
    label_seperator = ' | '

    # Expects a dictionary of [area: timedelta]
    def __init__(self, area_time_dict, max_width):
        self._print_graph(area_time_dict, max_width)

    def _print_graph(self, area_time_dict, max_width):

        # First, create the graph labels
        labels = dict(map(lambda x: (x[0], '{0} [{1}]'.format(x[0], c.format_time_delta(x[1]))), area_time_dict.items()))

        # Get the length of the longest label
        longest_label = len(max(labels.values(), key=len))

        for k, v in labels.items():
            if len(v) < longest_label:
                labels[k] = v + ' '*(longest_label-len(v)) + self.label_seperator
            else:
                labels[k] = v + self.label_seperator

        # Update the max width with the longest label
        max_width -= longest_label + len(self.label_seperator)

        # Convert the timedeltas into percentages
        largest_delta = max(area_time_dict.values())

        percentages = dict(map(lambda x: (x[0], x[1]/largest_delta), area_time_dict.items()))

        # Create the bars based on the percentages and max max_width

        bars = dict(map(lambda x: (x[0], round(max_width*x[1]) * self.bar_character), percentages.items()))

        # Print the labels and bars
        for k, v in labels.items():
            print('{0}{1}'.format(v, bars[k]))
