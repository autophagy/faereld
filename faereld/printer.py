# -*- coding: utf-8 -*-

"""
faereld.printer
---------------
"""

from . import utils

class String(object):

    def __init__(self, string):
        self.string = string
        self.final_line_length = len(string)

    def wrap(self, start, width):
        s = self.string
        strings = []
        if self.first_break() > width - start:
            strings.append('')
            start = 0
        while len(s) > width - start:
            # Find the first space before where the break should be
            pos = s[:width-start].rfind(' ')
            if pos == -1:
                # If no space exists just break on the word.
                pos = width - start - 1
            strings.append(s[:pos].strip())
            s = s[pos:].strip()
            start = 0
        strings.append(s)
        self.final_line_length = start + len(s)
        self.string = '\n'.join(strings)

    def first_break(self):
        first = self.string.find(' ')
        if first == -1:
            return len(self)
        return first

    def __str__(self):
        return self.string

    def __len__(self):
        return len(self.string)


class HighlightedString(String):

    def _highlighted(self):
        return "\033[94m{0}\033[0m".format(self.string)

    def __str__(self):
        return self._highlighted()


class Printer(object):

    def __init__(self):
        self.strings = []

    def add(self, text):
        self.strings.append(String(text))
        return self

    def add_highlighted(self, text):
        self.strings.append(HighlightedString(text))
        return self

    def print(self):
        width = utils.terminal_width()
        c = 0
        wrapped_strings = []
        # First wrap all the strings according to the width
        for string in self.strings:
            if string.first_break() + c > width:
                wrapped_strings.append('\n')
                c = 0
            string.wrap(c, width)
            wrapped_strings.append(string)
            c = string.final_line_length
        # Combine the wrapped strings
        final = ''.join(str(string) for string in wrapped_strings)
        print(final)
