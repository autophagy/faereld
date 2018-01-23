# -*- coding: utf-8 -*-

"""
faereld.utils
-----------

Various useful static functions and variables for use within Færeld.
"""

from math import floor
from shutil import get_terminal_size
from datetime import datetime
from textwrap import fill
import re

header = "FÆRELD :: {0} MODE"

def time_diff(from_date, to_date):
    diff_delta = to_date - from_date
    return format_time_delta(diff_delta)

def format_time_delta(time_delta):
    hours, remainder = divmod(time_delta.total_seconds(), 3600)
    minutes = floor(remainder/60)

    return "{0}h{1}m".format(floor(hours), minutes)

def print_rendered_string(area_code, area, date_to_display, object_name, duration):
    if type(date_to_display) is datetime:
        formatted_date = date_to_display.strftime("%d %b %Y")
    else:
        formatted_date = date_to_display.formatted()

    rendering_string = area['rendering_string'].format(area=highlight(area_code),
                                                       area_name=highlight(area['name']),
                                                       object=highlight(object_name),
                                                       date=highlight(formatted_date),
                                                       duration=highlight(duration))

    print_wordwrap(rendering_string)

def highlight(item):
    return "\033[94m{0}\033[0m".format(item)

def print_header(string):
    print("\033[91m{0} {1}\033[0m".format(string.upper(), "─"*(terminal_width() - len(string) - 1)))

def terminal_width():
    return get_terminal_size().columns

def max_width(max_config_width):
    return min(terminal_width(), max_config_width)

def print_wordwrap(*strings):
    string = ''.join(strings)
    stripped_len = len(strip_colour_codes(string))
    print(fill(string, terminal_width() + (len(string) - stripped_len)))

def strip_colour_codes(string):
    return re.sub('\x1b\[[0-9;]*m', '', string)

def print_areas_help(areas):
    for area_code, area in areas.items():
        print('{0} :: {1}'.format(area_code, area['name']))

def print_projects_help(projects):
    for project_code, project in projects.items():
        print('{0} :: {1} [{2}]'.format(project_code, project['name'], project['link']))
