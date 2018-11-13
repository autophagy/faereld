# -*- coding: utf-8 -*-
"""
faereld.controller
------------------

"""

from faereld.db import FaereldData
from faereld import utils
from faereld.printer import Printer, Highlight
from faereld import help

from os import path
import datarum
import datetime
import time
from functools import wraps

from prompt_toolkit import prompt
from prompt_toolkit.contrib.completers import WordCompleter


class CategoryValidator(object):
    HELP_CHAR = "?"

    def __init__(self, categories, category_type="Object", help_generator=None):
        self.categories = categories
        self.category_type = category_type
        self.help_generator = help_generator

    def validate(self, input):
        if self.help_generator is not None and input is self.HELP_CHAR:
            Printer().newline().print()
            self.help_generator().print()
            return False

        if input not in self.categories:
            Printer().newline().add(
                "Invalid {} :: ".format(self.category_type), Highlight(input)
            ).print()
            return False

        return True


class Controller(object):
    def __init__(self, config):
        self.config = config
        self.data_path = path.expanduser(self.config.get_data_path())
        self.db = FaereldData(self.data_path, self.config)

    def _time_function(self):
        @wraps(self)
        def wrapper(*args, **kwargs):
            begin = time.time()
            result = self(*args, **kwargs)
            end = time.time()
            print("\n[ {}ms ]".format(round((end - begin) * 100)))
            return result

        return wrapper

    # Summary Mode
    @_time_function
    def summary(self, target):
        summary = self.db.get_summary(target=target, detailed=True)
        if target is None:
            Printer().add_mode_header("Summary").print()
        else:
            if target not in self.config.get_areas():
                p = Printer()
                p.add("ERROR: No area found for: [", Highlight(target), "]")
                p.newline()
                p.add("Valid areas are: ")
                for area in self.config.get_areas():
                    p.add(f"[{area}]")
                p.print()
                return
            Printer().add_mode_header(f"Summary [{target}]").print()
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
        entry_inputs = None
        while entry_inputs is None:
            entry_inputs = self.gather_inputs()
        self.db.create_entry(**entry_inputs)
        print("Færeld entry added")

    def gather_inputs(self):
        Printer().newline().add_header("Area").newline().add(
            "[ {0} ]".format(" // ".join(self.config.get_areas().keys()))
        ).newline().print()
        area = self.input_area()
        if area in self.config.get_project_areas():
            Printer().newline().add_header("Project").newline().add(
                "[ {0} ]".format(" // ".join(sorted(self.config.get_projects().keys())))
            ).newline().print()
            object = self.input_project_object()
        else:
            Printer().newline().add_header("Object").newline().print()
            object = self.input_non_project_object(area)
        Printer().newline().add_header("Duration").newline().print()
        from_date, to_date = self.input_duration()
        time_diff = utils.time_diff(from_date, to_date)
        print()
        if self.config.get_use_wending:
            date_display = from_date.strftime("{daeg} {month} {gere}")
        else:
            date_display = from_date.strftime("%d %b %Y")
        if area in self.config.get_project_areas():
            Printer().newline().add_header("Purpose").newline().print()
            purpose = self.input_purpose()
        else:
            purpose = None
        utils.print_rendered_string(
            area,
            self.config.get_areas()[area],
            date_display,
            self.config.get_object_name(area, object),
            time_diff,
            purpose,
        )
        confirmation = prompt("Is this correct? (y/n) :: ", vi_mode=True)
        if confirmation.lower() == "y":
            return {
                "area": area,
                "object": object,
                "start": from_date,
                "end": to_date,
                "purpose": purpose,
            }

        else:
            return None

    def input_area(self):
        def area_help_generator():
            return help.areas_help(self.config.get_areas())

        area_completer = WordCompleter(self.config.get_areas().keys())
        area_validator = CategoryValidator(
            self.config.get_areas().keys(), "Area", area_help_generator
        )
        area = None
        while area is None:
            area_input = prompt(
                "Area :: ", completer=area_completer, vi_mode=True
            ).strip()
            if area_validator.validate(area_input):
                area = area_input
        return area

    def input_project_object(self):
        def project_help_generator():
            sorted_projects = sorted(self.config.get_projects().keys())
            project_descriptions = self.config.get_project_description
            return help.projects_help(sorted_projects, project_descriptions)

        projects = self.config.get_projects()
        project_completer = WordCompleter(sorted(projects.keys()))
        project_validator = CategoryValidator(
            projects.keys(), "Project", project_help_generator
        )
        project = None
        while project is None:
            project_input = prompt(
                "Project :: ", completer=project_completer, vi_mode=True
            )
            if project_validator.validate(project_input):
                project = project_input
        return project

    def input_non_project_object(self, area):
        use_last_objects = self.config.get_area(area).get("use_last_objects", False)
        last_objects = []
        if use_last_objects:
            last_objects = self.db.get_last_objects(
                area, self.config.get_num_last_objects()
            )
            last_objects_dict = {
                "[{0}]".format(x): k[0] for x, k in enumerate(last_objects)
            }
            # Transform last objects into [x]: object tags
            if len(last_objects) > 0:
                p = Printer()
                last_objects_dict = {
                    "[{0}]".format(x): k for x, k in enumerate(last_objects)
                }
                p.add("Last {0} {1} Objects :: ".format(len(last_objects), area))
                p.newline()
                for k, v in sorted(last_objects_dict.items()):
                    p.add("{0} {1}".format(k, v))
                p.newline()
                p.print()
        object = prompt(
            "Object :: ", completer=WordCompleter(last_objects), vi_mode=True
        )
        if use_last_objects:
            if object in last_objects_dict:
                return last_objects_dict[object]

        return object

    def input_duration(self):
        from_date = None
        to_date = None
        while from_date is None and to_date is None:
            while from_date is None:
                from_input = prompt("From :: ", vi_mode=True)
                from_date = self.convert_input_date(from_input)
            while to_date is None:
                to_input = prompt("To :: ", vi_mode=True)
                to_date = self.convert_input_date(to_input)
            if from_date >= to_date:
                print(
                    "Invalid Duration :: {0}".format(
                        utils.time_diff(from_date, to_date)
                    )
                )
                from_date = None
                to_date = None
        return from_date, to_date

    def input_purpose(self):
        return prompt("Purpose :: ", vi_mode=True)

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
                return datarum.wending.strptime(
                    date_string, "{daeg} {month} {gere} // {tid_zero}.{minute_zero}"
                )

        except (ValueError, AttributeError):
            print()
            print(
                "{} is an invalid date string. For example, it must be of"
                " the form: 13 Forst 226 // 16.15".format(date_string)
            )
            return None

    def _convert_gregorian_date(self, date_string):
        try:
            if date_string.lower() == "now":
                now = datetime.datetime.now().replace(second=0)
                return now

            else:
                return datetime.datetime.strptime(date_string, "%d %b %Y // %H.%M")

        except (ValueError, TypeError):
            print()
            print(
                "{} is an invalid date string. For example, it must be of"
                " the form: 3 Dec 226 // 16.15".format(date_string)
            )
            return None
