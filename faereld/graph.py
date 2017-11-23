# -*- coding: utf-8 -*-

"""
faereld.cli
-----------
"""

from . import utils
from numpy import percentile
from datetime import timedelta

class SummaryGraph(object):

    bar_character = '|'
    label_seperator = ' | '

    def __init__(self, area_values_map, max_width):
        self.area_values_map = area_values_map
        self.max_width = max_width

    def generate(self):

        # Total up the values
        area_total_dict = dict(map(lambda x: (x[0], sum(x[1], timedelta())), self.area_values_map.items()))

        # First, create the graph labels
        labels = dict(map(lambda x: (x[0], '{0} [{1}]'.format(x[0], utils.format_time_delta(x[1]))), area_total_dict.items()))

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


class BoxPlot(object):

    left_whisker = "┣"
    right_whisker = "┫"
    whisker = "━"
    box_body = "█"
    median = "#"
    formatted_median = "\033[91m█\033[0m"

    def __init__(self, area_values_map, max_width):
        self.area_values_map = area_values_map
        self.max_width = max_width

    def generate(self):

        # First, filter out any areas that have no values.
        area_values = dict(filter(lambda x: len(x[1]) > 0, self.area_values_map.items()))

        # Convert the timedeltas into ints
        for key, value in area_values.items():
            area_values[key] = list(map(lambda x: x.seconds, value))

        # Used to determine where to place things
        overall_min = None
        overall_max = None

        # Should be of the form key: (max, min, 1st quart, 2nd quart, 3rd quart)
        box_plot_tuples = { }

        for key, area_value in area_values.items():
            min_val = min(area_value)
            max_val = max(area_value)
            first = percentile(area_value, 25)
            second = percentile(area_value, 50)
            third = percentile(area_value, 75)
            box_plot_tuples[key] = (min_val, max_val, first, second, third)

            if overall_max is None or overall_min is None:
                overall_min = min_val
                overall_max = max_val

            if min_val < overall_min:
                overall_min = min_val

            if max_val > overall_max:
                overall_max = max_val

        # Transform the values to character positions from the minimum
        # Max width is reduced by 7 for 'KEY :: '
        max_width_bar = self.max_width - len('KEY :: ')

        for key, values in box_plot_tuples.items():
            positions = list(map(lambda x: int(round(max_width_bar*((x - overall_min) / (overall_max-overall_min)))), values))
            box_plot_tuples[key] = self._create_box_plot(*positions)

        # Merge the labels and the box plots into a single string
        returnable_list = list(map(lambda x: "{0} :: {1}\n".format(x[0], x[1]), box_plot_tuples.items()))

        # Add the min/max labels
        min_formatted = utils.format_time_delta(timedelta(0, overall_min))
        max_formatted = utils.format_time_delta(timedelta(0, overall_max))
        returnable_list.append("MIN :: {0} // MAX :: {1}".format(min_formatted,
                                                                 max_formatted))


        return returnable_list

    def _create_box_plot(self, min_pos, max_pos, first_pos, second_pos, third_pos):
        # First, pad out the string with spaces until the min
        box_string = " "*(min_pos-1)
        # Add the whisker
        box_string += self.left_whisker
        # Pad until the first quartile
        box_string += self.whisker*((first_pos-1)-len(box_string))
        # Pad until the second quartile
        box_string += self.box_body*((second_pos-1)-len(box_string))
        # Add the second quartile
        box_string += self.median
        # Pad until the third quartile
        box_string += self.box_body*(third_pos-len(box_string))
        # Pad until the max
        box_string += self.whisker*((max_pos-1)-len(box_string))
        # Add the whisker
        box_string += self.right_whisker

        # Format out the median character now we've created it
        box_string = box_string.replace(self.median, self.formatted_median)
        return box_string
