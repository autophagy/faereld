# -*- coding: utf-8 -*-

"""
faereld.cli
-----------
"""

import argparse

from .configuration import Configuration
from .controller import Controller


def parse_args():
    parser = argparse.ArgumentParser(description=('faereld :: personal project'
                                                 ' time tracker.'))
    parser.add_argument('-c', '--config',
                        default='~/.andgeloman/faereld/config.yml',
                        help='The faereld config file to use.')
    parser.add_argument('mode', metavar='mode', choices=['summary',
                                                      'insert',
                                                      'sync'],
                        help='Mode to run faereld in.')


    return parser.parse_args()


def main():
    try:
        args = parse_args()
        config = Configuration(args.config)
        controller = Controller(config)

        if args.mode == 'summary':
            controller.summary()
        elif args.mode == 'insert':
            controller.insert()
        elif args.mode == 'sync':
            controller.sync()

    except KeyboardInterrupt:
        exit(0)


if __name__ == '__main__':
    main()
