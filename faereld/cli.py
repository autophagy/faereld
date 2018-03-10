# -*- coding: utf-8 -*-

"""
faereld.cli
-----------
"""

import argparse

from .configuration import Configuration
from .controller import Controller
from . import utils
from .printer import Printer

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
            print("\x1b[2J\x1b[H", end="")
            config = Configuration(args.config)
            controller = Controller(config)
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
        print()
        p = Printer()
        p.add("Færeld (an Old English word meaning journey or ",
              "progession) is a time tracking utility built for ",
              "optimising and visualising the time spent on ",
              "projects and self-improvement.")
        p.newline()
        p.add("faereld [-c CONFIG] MODE")
        p.newline()
        p.add("Færeld has 5 modes:")
        p.add("INSERT       Insert a time tracking record into Færeld")
        p.add("SUMMARY      Produce a summary of time spent on all areas")
        p.add("PROJECTS     Produce a summary of time spent on project specific areas")
        p.add("PRODUCTIVITY Produce a summary of productivity aggregated over hours and days of the week")
        p.add("HELP         Print the help")
        p.newline()
        p.add_header("Configuration")
        p.newline()
        p.add("Færeld's configuration file is stored, by ",
              "default, in ~/.andgeloman/faereld/config.yml. ",
              "In this file you can define your own areas and ",
              "projects, as well as tweak some settings for ",
              "things like the data path. For a full ",
              "explanation of these settings, please consult ",
              "https://faereld.readthedocs.io/en/latest/usage/configuration.html.")
        p.newline()
        p.add("To use a different configuration file, use the -c flag ::")
        p.add("    faereld -c /path/to/config.yml MODE")
        p.newline()
        p.add("Source :: https://github.com/autophagy/faereld")
        p.add("Issue Tracker :: https://github.com/autophagy/faereld/issues")
        p.add("Documentation :: https://faereld.readthedocs.io/en/latest/")
        p.print()

def main():
    try:
        Faereld()
    except KeyboardInterrupt:
        print("\n\nExiting...\n")
        exit(0)
