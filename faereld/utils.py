# -*- coding: utf-8 -*-

"""
faereld.utils
-----------

Various useful static functions and variables for use within Færeld.
"""

from math import floor
from os import get_terminal_size


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
    'LNG': 'Languages'
}

areas = project_areas.copy()
areas.update(misc_areas)

rendering_strings = {
    'projects': 'On \033[94m{0}\033[0m I worked on \033[94m{1}\033[0m (\033[94m{2}\033[0m) for \033[94m{3}\033[0m',
    'IRL': 'On \033[94m{0}\033[0m I was at \033[94m{1}\033[0m for \033[94m{2}\033[0m',
    'RDG': 'On \033[94m{0}\033[0m I read \033[94m{1}\033[0m for \033[94m{2}\033[0m',
    'LNG': 'On \033[94m{0}\033[0m I studied \033[94m{1}\033[0m for \033[94m{2}\033[0m'
}

header = "FÆRELD :: {0} MODE"

def time_diff(from_date, to_date):
    diff_delta = to_date - from_date
    return format_time_delta(diff_delta)

def format_time_delta(time_delta):
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes = floor(remainder/60)

    return "{0}h{1}m".format(hours, minutes)

def print_rendered_string(area, wending_date, object, time_diff):
    if area in project_areas:
        print(rendering_strings['projects'].format(wending_date.formatted(),
                                                   object,
                                                   areas[area],
                                                   time_diff))
    else:
        print(rendering_strings[area].format(wending_date.formatted(),
                                             object,
                                             time_diff))

def print_header(string):
    width = get_terminal_size().columns
    print("\033[91m{0} {1}\033[0m".format(string, "─"*(width - len(string) - 3)))
