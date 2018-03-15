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
from . import help

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
        help.cli_help().print()

def main():
    try:
        Faereld()
    except KeyboardInterrupt:
        print("\n\nExiting...\n")
        exit(0)
