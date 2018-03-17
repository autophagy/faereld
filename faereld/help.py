# -*- coding: utf-8 -*-
"""
faereld.help
-----------

Help
"""

from faereld.printer import Printer


def projects_help(projects, project_description_func):
    p = Printer()
    for project in projects:
        p.add('[{}]'.format(project))
        p.add(project_description_func(project))
        p.newline()
    return p


def areas_help(areas):
    p = Printer()
    for area_code, area in areas.items():
        p.add('[{0}] {1}'.format(area_code, area['name']))
    p.newline()
    return p


def cli_help():
    p = Printer()
    p.add_mode_header("Help")
    p.newline()
    p.add(
        "Færeld (an Old English word meaning journey or ",
        "progession) is a time tracking utility built for ",
        "optimising and visualising the time spent on ",
        "projects and self-improvement.",
    )
    p.newline()
    p.add("faereld [-c CONFIG] MODE")
    p.newline()
    p.add("Færeld has 5 modes:")
    p.add("INSERT       Insert a time tracking record into Færeld")
    p.add("SUMMARY      Produce a summary of time spent on all areas")
    p.add("PROJECTS     Produce a summary of time spent on project specific areas")
    p.add(
        "PRODUCTIVITY Produce a summary of productivity aggregated over ",
        "hours and days of the week",
    )
    p.add("HELP         Print the help")
    p.newline()
    p.add_header("Configuration")
    p.newline()
    p.add(
        "Færeld's configuration file is stored, by ",
        "default, in ~/.andgeloman/faereld/config.yml. ",
        "In this file you can define your own areas and ",
        "projects, as well as tweak some settings for ",
        "things like the data path. For a full ",
        "explanation of these settings, please consult ",
        "https://faereld.readthedocs.io/en/latest/usage/configuration.html.",
    )
    p.newline()
    p.add("To use a different configuration file, use the -c flag ::")
    p.add("    faereld -c /path/to/config.yml MODE")
    p.newline()
    p.add("Source :: https://github.com/autophagy/faereld")
    p.add("Issue Tracker :: https://github.com/autophagy/faereld/issues")
    p.add("Documentation :: https://faereld.readthedocs.io/en/latest/")
    return p
