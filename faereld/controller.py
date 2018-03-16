# -*- coding: utf-8 -*-

"""
faereld.controller
------------------

"""

from .db import FaereldData
from . import utils
from .printer import Printer
from . import help

from os import path
import datarum
import datetime
import time
from functools import wraps

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter

class Controller(object):

    def __init__(self, config):
        self.config = config
        self.data_path = path.expanduser(self.config.get_data_path())
        self.db = FaereldData(self.data_path, self.config)

    def _time_function(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            begin = time.time()
            result = func(*args, **kwargs)
            end = time.time()

            print("\n[ {}ms ]".format(round((end-begin)*100)))
            return result
        return wrapper

    # Summary Mode

    @_time_function
    def summary(self):
        summary = self.db.get_summary(detailed=True)
        Printer().add_mode_header("Summary").print()
        summary.print()

    # Projects Summary Mode

    @_time_function
    def projects(self):
        projects_summary = self.db.get_projects_summary()
        Printer().add_mode_header("Projects Summary").print()
        projects_summary.print()

    # Productivity Summary Mode

    @_time_function
    def productivity(self):
        productivity_summary = self.db.get_productivity_summary()
        Printer().add_mode_header("Productivity Summary").print()
        productivity_summary.print()

    # Insert Mode

    def insert(self):
        Printer().add_mode_header("Insert").print()

        summary = self.db.get_summary()
        summary.print()

        print()

        Printer() \
         .add_header('Area') \
         .newline() \
         .add("[ {0} ]".format(' // '.join(self.config.get_areas().keys()))) \
         .newline() \
         .print()

        area_completer = WordCompleter(self.config.get_areas().keys())
        area = prompt('Area :: ', completer=area_completer, vi_mode=True)

        while area not in self.config.get_areas():
            print()
            if area == '?':
                help.areas_help(self.config.get_areas()).print()
            else:
                print("Invalid Area :: {0}".format(area))
            area = prompt('Area :: ', completer=area_completer, vi_mode=True)

        if area in self.config.get_project_areas():
            object = self._project_object()
        else:
            object = self._non_project_object(area)

        Printer() \
         .newline() \
         .add_header('Duration') \
         .newline() \
         .print() \

        # Assume to be in the form [date // time]
        date_to_display = None

        from_date = None
        to_date = None

        while from_date is None and to_date is None:
            while from_date is None:
                from_input = prompt('From :: ', vi_mode=True)
                from_date = self.convert_input_date(from_input)

            while to_date is None:
                to_input = prompt('To :: ', vi_mode=True)
                to_date = self.convert_input_date(to_input)

            time_diff = utils.time_diff(from_date, to_date)

            if from_date >= to_date:
                print("Invalid Duration :: {0}".format(time_diff))
                from_date = None
                to_date = None

        print()

        if self.config.get_use_wending:
            date_display = from_date.strftime('{daeg} {month} {gere}')
        else:
            date_display = from_date.strftime('%d %b %Y')
        utils.print_rendered_string(area,
                                    self.config.get_areas()[area],
                                    date_display,
                                    self.config.get_object_name(area, object),
                                    time_diff)

        confirmation = prompt("Is this correct? (y/n) :: ", vi_mode=True)

        if confirmation.lower() == 'y':
            self.db.create_entry(area,
                                 object,
                                 from_date,
                                 to_date)

            print("Færeld entry added")
        else:
            print("Færeld entry cancelled")

    def _project_object(self):
        projects = self.config.get_projects()

        print()
        Printer() \
         .add_header('Project') \
         .newline() \
         .add("[ {0} ]".format(' // '.join(sorted(projects.keys())))) \
         .newline() \
         .print()

        project_completer = WordCompleter(sorted(projects.keys()))
        project = prompt('Project :: ', completer=project_completer, vi_mode=True)

        while project not in projects:
            print()
            if project == '?':
                k = sorted(projects.keys())
                f = self.config.get_project_description
                help.projects_help(k, f).print()
            else:
                print("Invalid Project :: {0}".format(project))
            project = prompt('Project :: ', completer=project_completer, vi_mode=True)

        return project

    def _non_project_object(self, area):

        use_last_objects = self.config.get_area(area).get('use_last_objects', False)
        print()
        p = Printer()
        p.add_header('Object')
        p.newline()

        last_objects = []

        if use_last_objects:
            last_objects = self.db.get_last_objects(area, self.config.get_num_last_objects())

            last_objects_dict = {'[{0}]'.format(x): k[0] for x, k in enumerate(last_objects)}

            # Transform last objects into [x]: object tags
            if len(last_objects) > 0:
                last_objects_dict = {'[{0}]'.format(x): k for x, k in enumerate(last_objects)}
                p.add("Last {0} {1} Objects :: ".format(len(last_objects), area))
                p.newline()
                for k, v in sorted(last_objects_dict.items()):
                    p.add("{0} {1}".format(k, v))
                p.newline()

        p.print()

        object = prompt('Object :: ', completer=WordCompleter(last_objects), vi_mode=True)

        if use_last_objects:
            if object in last_objects_dict:
                return (last_objects_dict[object])

        return object

    def convert_input_date(self, date_string):
        if self.config.get_use_wending():
            return self._convert_wending_date(date_string)
        else:
            return self._convert_gregorian_date(date_string)

    def _convert_wending_date(self, date_string):
        try:
            if date_string.lower() == "now":
                now = datarum.wending.now().replace(second=0)
                return now
            else:
                return datarum.wending.strptime(date_string,
                                                "{daeg} {month} {gere} // {tid_zero}.{minute_zero}")
        except (ValueError, AttributeError):
            print()
            print("{} is an invalid date string. For example, it must be of"
                  " the form: 13 Forst 226 // 16.15".format(date_string))
            return None

    def _convert_gregorian_date(self, date_string):
        try:
            if date_string.lower() == "now":
                now = datetime.datetime.now().replace(second=0)
                return now
            else:
                return datetime.datetime.strptime(date_string,
                                                        "%d %b %Y // %H.%M")
        except (ValueError, TypeError):
            print()
            print("{} is an invalid date string. For example, it must be of"
                  " the form: 3 Dec 226 // 16.15".format(date_string))
            return None
