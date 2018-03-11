# -*- coding: utf-8 -*-

"""
faereld.summaries.simple
-----------------------

A summary to provide brief detail about the Faereld data.
"""

from ..printer import Printer

class SimpleSummary(object):

        def __init__(self, days, entries, formatted_time):
            self.days = days
            self.entries = entries
            self.formatted_time = formatted_time

        def print(self):
            summary = "{0} DAYS // {1} ENTRIES // TOTAL {2}"
            p = Printer()
            p.add_header(summary.format(self.days,
                                        self.entries,
                                        self.formatted_time))
            p.print()
