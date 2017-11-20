# -*- coding: utf-8 -*-

"""
faereld.utils
-----------

Various useful static functions and variables for use within Færeld.
"""

from math import floor


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
    'LNG': 'On \033[94m{0}\033[0m I learned \033[94m{1}\033[0m for \033[94m{2}\033[0m'
}

header = "FÆRELD :: {0} MODE"

def format_time_delta(time_delta):
    hours, remainder = divmod(time_delta.seconds, 3600)
    minutes = floor(remainder/60)

    return "{0}h{1}m".format(hours, minutes)
