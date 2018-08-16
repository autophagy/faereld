# -*- coding: utf-8 -*-
"""
faereld.printer
---------------
"""

from shutil import get_terminal_size


class String(object):
    def __init__(self, *string):
        self.string = "".join(string)
        self.final_line_length = len(string)

    def wrap(self, start, width):
        s = self.string
        strings = []
        if self.first_break() > width - start:
            strings.append("")
            start = 0
        while len(s) > width - start:
            # Find the first space before where the break should be
            pos = s[: width - start].rfind(" ")
            if pos == -1:
                # If no space exists just break on the word.
                pos = width - start - 1
            strings.append(s[:pos].strip())
            s = s[pos:].strip()
            start = 0
        strings.append(s)
        self.final_line_length = start + len(s)
        self.string = "\n".join(strings)

    def first_break(self):
        first = self.string.find(" ")
        if first == -1:
            return len(self)

        return first

    def __str__(self):
        return self.string

    def __len__(self):
        return len(self.string)


class Highlight(String):
    def _highlighted(self):
        return "\033[94m{0}\033[0m".format(self.string)

    def __str__(self):
        return self._highlighted()


class Header(String):
    def _headerised(self):
        return "\033[91m{0}\033[0m".format(self.string)

    def __str__(self):
        return self._headerised()


class Unwrappable(String):

    # Only use this class when you absolutely do not need the string to wrap.
    # For example, in use with graphs, where the graph is already calculated
    # to fit within the terminal.
    def wrap(self, width, start):
        pass


class Printer(object):
    def __init__(self):
        self.paragraphs = []

    def add(self, *texts):
        p = []
        for text in texts:
            if type(text) is Highlight:
                p.append(text)
            else:
                p.append(String(text))
        self.paragraphs.append(p)
        return self

    def newline(self):
        self.paragraphs.append([String("")])
        return self

    def add_header(self, text):
        self.paragraphs.append(
            [
                Header(
                    "{0} {1}".format(
                        text.upper(), "─" * (self._width() - len(text) - 1)
                    )
                )
            ]
        )
        return self

    def add_mode_header(self, text):
        mode_header = "Færeld :: {0} Mode"
        return self.add_header(mode_header.format(text))

    def add_nowrap(self, text):
        self.paragraphs.append([Unwrappable(text)])
        return self

    def _format_printer_contents(self):
        width = self._width()
        lines = []
        for paragraph in self.paragraphs:
            c = 0
            wrapped_strings = []
            # First wrap all the strings according to the width
            for string in paragraph:
                if string.first_break() + c > width:
                    wrapped_strings.append("\n")
                    c = 0
                string.wrap(c, width)
                wrapped_strings.append(string)
                c = string.final_line_length
            # Combine the wrapped strings
            lines.append("".join(str(string) for string in wrapped_strings))
        return lines

    def print(self):
        lines = self._format_printer_contents()
        for line in lines:
            print(line)

    def __str__(self):
        return "\n".join(self._format_printer_contents())

    def _width(self):
        return get_terminal_size().columns
