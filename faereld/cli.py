# -*- coding: utf-8 -*-
"""
faereld.cli
-----------
"""

import argparse

from faereld.configuration import Configuration
from faereld.controller import Controller
from faereld import help
from faereld.printer import Printer, Highlight


class Faereld(object):

    def __init__(self):
        parser = argparse.ArgumentParser(
            add_help=False,
            description=(
                "Færeld :: A time tracking utility for effort optimisation ",
                "and visualisation",
            ),
        )
        parser.add_argument(
            '-c', '--config', default='~/.andgeloman/faereld/config.yml'
        )
        parser.add_argument('mode', help="Mode to run")
        args = parser.parse_args()
        if not hasattr(self, args.mode.lower()):
            Printer().add(*parser.description).newline().add(
                Highlight(args.mode), " is an unrecognised mode."
            ).newline().print()
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
        print("\nExiting...\n")
        exit(0)
