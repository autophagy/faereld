# -*- coding: utf-8 -*-
"""
faereld.cli
-----------
"""

import argparse

from faereld import help
from faereld.configuration import Configuration
from faereld.controller import Controller
from faereld.printer import Highlight, Printer


class Faereld(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            add_help=False,
            description=(
                "Færeld :: A time tracking utility for effort optimisation ",
                "and visualisation",
            ),
            usage="\n" + str(help.cli_help()),
        )
        parser.add_argument(
            "-c", "--config", default="~/.andgeloman/faereld/config.yml"
        )
        parser.add_argument("mode", help="Mode to run")
        parser.add_argument("target", nargs="?", help="Target for the mode")
        args = parser.parse_args()
        if not hasattr(self, args.mode.lower()):
            Printer().add(*parser.description).newline().add(
                Highlight(args.mode), " is an unrecognised mode."
            ).newline().print()
            self.help()
            exit(1)
        else:
            print("\x1b[2J\x1b[H", end="")
            config = Configuration(args.config)
            controller = Controller(config)
            getattr(self, args.mode.lower())(controller=controller, target=args.target)

    @staticmethod
    def insert(controller, *args, **kwargs):
        controller.insert()

    @staticmethod
    def summary(controller, *args, **kwargs):
        controller.summary(kwargs.get("target"))

    @staticmethod
    def projects(controller, *args, **kwargs):
        controller.projects()

    @staticmethod
    def productivity(controller, *args, **kwargs):
        controller.productivity()

    @staticmethod
    def help(*args, **kwargs):
        help.cli_help().print()


def main():
    try:
        Faereld()
    except KeyboardInterrupt:
        print("\nExiting...\n")
        exit(0)
