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


project_areas = {
    'RES': 'Research',
    'DES': 'Design',
    'DEV': 'Development',
    'DOC': 'Documentation',
    'TST': 'Testing',
}

misc_areas = {
    'IRL': 'Real life engagements (confs/talks/meetups)',
    'RDG': 'Reading',
    'LNG': 'Languages',
    'TSK': 'Tasks'
}

areas = project_areas.copy()
areas.update(misc_areas)

rendering_strings = {
    'projects': 'On \033[94m{0}\033[0m I worked on \033[94m{1}\033[0m (\033[94m{2}\033[0m) for \033[94m{3}\033[0m',
    'IRL': 'On \033[94m{0}\033[0m I was at \033[94m{1}\033[0m for \033[94m{2}\033[0m',
    'RDG': 'On \033[94m{0}\033[0m I read \033[94m{1}\033[0m for \033[94m{2}\033[0m',
    'LNG': 'On \033[94m{0}\033[0m I studied \033[94m{1}\033[0m for \033[94m{2}\033[0m',
    'TSK': 'On \033[94m{0}\033[0m I worked on \033[94m{1}\033[0m for \033[94m{2}\033[0m'
}

header = "FÆRELD :: {0} MODE"

def time_diff(from_date, to_date):
    diff_delta = to_date - from_date
    return format_time_delta(diff_delta)

def format_time_delta(time_delta):
    hours, remainder = divmod(time_delta.total_seconds(), 3600)
    minutes = floor(remainder/60)

    return "{0}h{1}m".format(floor(hours), minutes)

def print_rendered_string(area, date_to_display, object, time_diff):

    if type(date_to_display) is datetime:
        formatted_date = date_to_display.strftime("%d %b %Y")
    else:
        formatted_date = date_to_display.formatted()

    if area in project_areas:
        print_wordwrap(rendering_strings['projects'].format(formatted_date,
                                                            object,
                                                            areas[area],
                                                            time_diff))
    else:
        print_wordwrap(rendering_strings[area].format(formatted_date,
                                                      object,
                                                      time_diff))

def print_header(string):
    print("\033[91m{0} {1}\033[0m".format(string, "─"*(terminal_width() - len(string) - 1)))

def terminal_width():
    return get_terminal_size().columns

def print_wordwrap(string):
    stripped_len = len(strip_colour_codes(string))
    print(fill(string, terminal_width() + (len(string) - stripped_len)))

def strip_colour_codes(string):
    return re.sub('\x1b\[[0-9;]*m', '', string)

def print_areas_help():
    for area, desc in areas.items():
        print('{0} :: {1}'.format(area, desc))
