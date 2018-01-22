# -*- coding: utf-8 -*-

"""
faereld.cli
-----------
"""

import argparse

from .configuration import Configuration
from .controller import Controller

class Faereld(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            add_help=False,
            description="Færeld :: A time tracking utility for effort optimisation and visualisation",
            usage='''faereld [-c CONFIG] mode

Færeld has 4 modes:
   insert       Insert a time tracking record into Færeld
   summary      Produce a summary of time spent on all areas
   projects     Produce a summary of time spent on project specific areas
''')

        parser.add_argument('-c', '--config', default='~/.andgeloman/faereld/config.yml')
        parser.add_argument('mode', help="Mode to run")
        args = parser.parse_args()
        if not hasattr(self, args.mode):
            print(parser.description)
            print()
            print("\033[91m{0}\033[0m is an unrecognised mode.\n".format(args.mode))
            print(parser.usage)
            exit(1)
        else:
            config = Configuration(args.config)
            controller = Controller(config)
            getattr(self, args.mode)(controller)


    def insert(self, controller):
        controller.insert()

    def summary(self, controller):
        controller.summary()

    def projects(self, controller):
        controller.projects()

def main():
    try:
        Faereld()
    except KeyboardInterrupt:
        print("\n\nExiting...\n")
        exit(0)
