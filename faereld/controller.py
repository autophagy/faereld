# -*- coding: utf-8 -*-
"""
faereld.controller
------------------

"""

import time
from functools import wraps
from os import path

from faereld import help, utils
from faereld.db import FaereldData
from faereld.input import DurationInput, Input
from faereld.printer import Highlight, Printer
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
                f"Invalid {self.category_type} :: ", Highlight(input)
            ).print()
            return False

        return True


class Entry:
    area = None
    object = None
    from_date = None
    to_date = None
    purpose = None

    def __init__(self, config):
        self.config = config

    def __str__(self):
        date_display = (
            self.from_date.strftime("{daeg} {month} {gere}")
            if self.config.use_wending
            else self.from_date.strftime("%d %b %Y")
        )
        duration = utils.time_diff(self.from_date, self.to_date)
        rendered_string = utils.get_rendered_string(
            self.area,
            self.config.get_area(self.area),
            date_display,
            self.config.get_object_name(self.area, self.object),
            duration,
            self.purpose,
        )
        return "".join(str(s) for s in rendered_string)


class Controller(object):
    def __init__(self, config):
        self.config = config
        self.data_path = path.expanduser(self.config.data_path)
        self.db = FaereldData(self.data_path, self.config)

    def _time_function(self):
        @wraps(self)
        def wrapper(*args, **kwargs):
            begin = time.time()
            result = self(*args, **kwargs)
            end = time.time()
            print(f"\n[ {round((end - begin) * 100)}ms ]")
            return result

        return wrapper

    # Summary Mode
    @_time_function
    def summary(self, target):
        summary = self.db.get_summary(target=target, detailed=True)
        if target is None:
            Printer().add_mode_header("Summary").print()
        else:
            if target not in self.config.areas:
                p = Printer()
                p.add("ERROR: No area found for: [", Highlight(target), "]")
                p.newline()
                p.add("Valid areas are: ")
                for area in self.config.areas:
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
        entry = None
        while entry is None:
            entry = Entry(self.config)

            Printer().newline().add_header("Area").newline().add(
                f"[ {' // '.join(self.config.areas.keys())} ]"
            ).newline().print()
            entry.area = self.input_area()
            if entry.area in self.config.project_areas:
                Printer().newline().add_header("Project").newline().add(
                    f"[ {' // '.join(sorted(self.config.projects.keys()))} ]"
                ).newline().print()
                entry.object = self.input_project_object()
            else:
                Printer().newline().add_header("Object").newline().print()
                entry.object = self.input_non_project_object(entry.area)

            duration_input = DurationInput(
                name="Duration", use_wending=self.config.use_wending
            )
            entry.from_date, entry.to_date = duration_input.gather()

            if entry.area in self.config.project_areas:
                purpose = Input(name="Purpose")
                entry.purpose = purpose.gather()
            else:
                entry.purpose = None
            print()
            print(str(entry))
            confirmation = prompt("Is this correct? (Y/n) :: ", vi_mode=True)
            if confirmation in ["Y", "y", ""]:
                break
            else:
                entry = None
        self.db.create_entry(entry)
        print("Færeld entry added")

    def input_area(self):
        def area_help_generator():
            return help.areas_help(self.config.areas)

        area_completer = WordCompleter(self.config.areas.keys())
        area_validator = CategoryValidator(
            self.config.areas.keys(), "Area", area_help_generator
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
            sorted_projects = sorted(self.config.projects.keys())
            project_descriptions = self.config.get_project_description
            return help.projects_help(sorted_projects, project_descriptions)

        projects = self.config.projects
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
            last_objects = self.db.get_last_objects(area, self.config.num_last_objects)
            last_objects_dict = {f"[{x}]": k[0] for x, k in enumerate(last_objects)}
            # Transform last objects into [x]: object tags
            if len(last_objects) > 0:
                p = Printer()
                last_objects_dict = {f"[{x}]": k for x, k in enumerate(last_objects)}
                p.add(f"Last {len(last_objects)} {area} Objects :: ")
                p.newline()
                for k, v in sorted(last_objects_dict.items()):
                    p.add(f"{k} {v}")
                p.newline()
                p.print()
        object = prompt(
            "Object :: ", completer=WordCompleter(last_objects), vi_mode=True
        )
        if use_last_objects:
            if object in last_objects_dict:
                return last_objects_dict[object]

        return object
