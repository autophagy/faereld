# -*- coding: utf-8 -*-

"""
faereld.cli
-----------
"""

import argparse

from .configuration import Configuration
from .controller import Controller
from . import utils

class Faereld(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            add_help=False,
            description="Færeld :: A time tracking utility for effort optimisation and visualisation")

        parser.add_argument('-c', '--config', default='~/.andgeloman/faereld/config.yml')
        parser.add_argument('mode', help="Mode to run")
        args = parser.parse_args()
        if not hasattr(self, args.mode.lower()):
            print(parser.description)
            print()
            print("\033[91m{0}\033[0m is an unrecognised mode.\n".format(args.mode))
            self.help(None)
            exit(1)
        else:
            config = Configuration(args.config)
            controller = Controller(config)
            print("\x1b[2J\x1b[H", end="")
            getattr(self, args.mode.lower())(controller)


    def insert(self, controller):
        controller.insert()

    def summary(self, controller):
        controller.summary()

    def projects(self, controller):
        controller.projects()

    def productivity(self, controller):
        controller.productivity()

    def help(self, _):
        utils.print_header(utils.header.format("Help"))
        utils.print_wordwrap("\nFæreld (an Old English word meaning journey or ",
                             "progession) is a time tracking utility built for ",
                             "optimising and visualising the time spent on ",
                             "projects and self-improvement.")
        utils.print_wordwrap('''
faereld [-c CONFIG] MODE

Færeld has 5 modes:
   INSERT       Insert a time tracking record into Færeld
   SUMMARY      Produce a summary of time spent on all areas
   PROJECTS     Produce a summary of time spent on project specific areas
   PRODUCTIVITY Produce a summary of productivity aggregated over hours and days of the week
   HELP         Print the help''')

        print()
        utils.print_header("Configuration")
        utils.print_wordwrap("\nFæreld's configuration file is stored, by ",
                             "default, in ~/.andgeloman/faereld/config.yml. ",
                             "In this file you can define your own areas and ",
                             "projects, as well as tweak some settings for ",
                             "things like the data path. For a full ",
                             "explanation of these settings, please consult ",
                             "https://faereld.readthedocs.io/en/latest/usage/configuration.html.")
        utils.print_wordwrap("\nTo use a different configuration file, use the -c flag ::")
        utils.print_wordwrap("    faereld -c /path/to/config.yml MODE")
        utils.print_wordwrap('''
Source :: https://github.com/autophagy/faereld
Issue Tracker :: https://github.com/autophagy/faereld/issues
Documentation :: https://faereld.readthedocs.io/en/latest/''')

def main():
    try:
        Faereld()
    except KeyboardInterrupt:
        print("\n\nExiting...\n")
        exit(0)
