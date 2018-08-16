# -*- coding: utf-8 -*-
"""
faereld.configuration
------------------

"""

from os import path, makedirs
from collections import OrderedDict
import yaml
from faereld.printer import Printer, Highlight


class Configuration(object):
    # Default Configuration Options
    DEFAULT_DATA_OPTIONS = {
        "data_path": "~/.andgeloman/faereld/faereld.hord",
        "use_wending": False,
        "num_last_objects": 5,
    }
    # Default Project Areas
    DEFAULT_RENDERING = "On {date} I worked on {object} ({area_name}) for {duration}"
    DEFAULT_PROJECT_AREAS = {
        "RES": {"name": "Research", "rendering_string": DEFAULT_RENDERING},
        "DES": {"name": "Design", "rendering_string": DEFAULT_RENDERING},
        "DEV": {"name": "Development", "rendering_string": DEFAULT_RENDERING},
        "DOC": {"name": "Documentation", "rendering_string": DEFAULT_RENDERING},
        "TST": {"name": "Testing", "rendering_string": DEFAULT_RENDERING},
    }
    # Default Projects
    DEFAULT_PROJECTS = {
        "faereld": {
            "name": "Færeld",
            "link": "https://github.com/Autophagy/faereld",
            "description": "A time tracking tool. ",
        }
    }
    # Default General Areas
    DEFAULT_GENERAL_AREAS = {
        "IRL": {
            "name": "Real life engagements (confs/talks/meetups)",
            "rendering_string": "On {date} I was at {object} for {duration}",
            "use_last_objects": False,
        },
        "RDG": {
            "name": "Reading",
            "rendering_string": "On {date} I read {object} for {duration}",
            "use_last_objects": True,
        },
        "LNG": {
            "name": "Languages",
            "rendering_string": "On {date} I studied {object} for {duration}",
            "use_last_objects": True,
        },
        "TSK": {
            "name": "Tasks",
            "rendering_string": "On {date} I worked on {object} for {duration}",
            "use_last_objects": False,
        },
    }
    # Default Summary Options
    DEFAULT_SUMMARY_OPTIONS = {
        "max_graph_width": 100,
        "exclude_from_total_time": ["TSK"],
        "exclude_from_entry_time_distribution": ["IRL"],
    }
    DEFAULT_CONFIG = {
        "data_options": DEFAULT_DATA_OPTIONS,
        "summary_options": DEFAULT_SUMMARY_OPTIONS,
        "project_areas": DEFAULT_PROJECT_AREAS,
        "projects": DEFAULT_PROJECTS,
        "general_areas": DEFAULT_GENERAL_AREAS,
    }
    # The configs defined here must have values set for their defaults.
    # For configs excluded from this group, the defaults are just examples.
    MUST_BE_PRESENT_CONFIGS = ["data_options", "summary_options"]
    # Banner to prepend to the default configuration if it does not exist.
    CONFIG_BANNER = """# Færeld :: Configuration File
#
# Please see
# https://faereld.readthedocs.io/en/latest/usage/configuration.html for a
# complete reference of configuration options, as well as their effects.

"""
    # Headers to prepend each config section
    CONFIG_AREA_HEADERS = {
        "data_options": """# data_options :: Settings For Data Options""",
        "summary_options": """# summary_options :: Settings For Summary Mode""",
        "project_areas": """# project_areas :: Definitions For Project-Specific Areas
#
# Project area definitions should be in the form:
# code:
#   name: Area Name
#   rendering_string: On {date} I worked on {object} for {duration}
#
# See https://faereld.readthedocs.io/en/latest/usage/configuration.html#project-areas
# for more information.""",
        "projects": """# projects :: Project Object Definitions
#
# A project definition should be of the form
# code:
#   name: Project Name
#   link: <link to project homepage>
#   desc: Project description
""",
        "general_areas": """# general_areas :: Definitions For General Areas
#
# Area definitions should be in the form:
# code:
#   name: Area Name
#   rendering_string: On {date} I worked on {object} for {duration}
#   use_last_objects: false
#
# See https://faereld.readthedocs.io/en/latest/usage/configuration.html#general-areas
# for more information.""",
    }

    def __init__(self, configuration_path):
        """ On initialisation, preload the configuration options from the
        defaults.
        """
        self.data_options = self.DEFAULT_DATA_OPTIONS
        self.project_areas = self.DEFAULT_PROJECT_AREAS
        self.projects = self.DEFAULT_PROJECTS
        self.general_areas = self.DEFAULT_GENERAL_AREAS
        self.summary_options = self.DEFAULT_SUMMARY_OPTIONS
        yaml.SafeDumper.add_representer(OrderedDict, self.__rep_odict)
        self.__load_configuration(configuration_path)

    def __load_configuration(self, configuration_path):
        """ Load the configuration from the supplied path. If the file does
        not exist at this path, create it from the default config settings.
        """
        expanded_path = path.expanduser(configuration_path)
        if not path.exists(path.dirname(expanded_path)):
            makedirs(path.dirname(expanded_path))
        if not path.exists(expanded_path):
            self.__write_config_file(expanded_path, self.DEFAULT_CONFIG)
            p = Printer()
            p.add_header("Wilcume on Færeld")
            p.newline()
            p.add("This looks like it is your first time running Færeld.")
            p.newline()
            p.add("A config file has been created at ", Highlight(expanded_path), ".")
            p.newline()
            p.add(
                "This contains some default values to get you started, ",
                "but you should take a look to add your own areas and projects.",
            )
            p.newline()
            p.add(
                "For more information, please see the configuration documentation ",
                "at https://faereld.readthedocs.io/en/latest/usage/configuration.html",
            )
            p.newline()
            p.print()
        else:
            self.__load_configuration_values(expanded_path)

    def __load_configuration_values(self, path):
        """ Load the configuration file, update the config values from this
        file.
        """
        config_variables = {
            "data_options": self.data_options,
            "summary_options": self.summary_options,
            "project_areas": self.project_areas,
            "projects": self.projects,
            "general_areas": self.general_areas,
        }
        with open(path, "r") as config_file:
            config_dict = yaml.load(config_file)
            if config_dict is None:
                config_dict = {}
            for key, value in config_variables.items():
                self.__update_configuration(key, config_dict, value)
        self.__write_config_file(path, config_variables)

    def __update_configuration(self, config_key, config_dict, var):
        """ Update a config dictionary given a category key
        """
        if config_key in config_dict:
            if config_key in self.MUST_BE_PRESENT_CONFIGS:
                # The values defined in the defaults must be present for these
                # config options.
                var.update(config_dict[config_key])
            else:
                # The values defined in the defaults are just examples, and do
                # not need to be present.
                var.clear()
                var.update(self.__validate_dict(config_dict[config_key]))

    def __rep_odict(self, dumper, data):
        """ Allows the yaml dumper to represent a OrderedDict, so that config
        item ordering is preserved."""
        v = []
        for k, val in data.items():
            item_key = dumper.represent_data(k)
            item_val = dumper.represent_data(val)
            v.append((item_key, item_val))
        return yaml.nodes.MappingNode(u"tag:yaml.org,2002:map", v)

    def __write_config_file(self, path, config):
        with open(path, "w") as config_file:
            config_file.write(self.CONFIG_BANNER)
            for key, value in config.items():
                config_file.write(self.CONFIG_AREA_HEADERS[key])
                config_file.write("\n")
                yaml.safe_dump(
                    {key: OrderedDict(value)},
                    config_file,
                    default_flow_style=False,
                    allow_unicode=True,
                )
                config_file.write("\n")

    def get_data_path(self):
        return self.data_options["data_path"]

    def get_use_wending(self):
        return self.data_options["use_wending"]

    def get_num_last_objects(self):
        return self.data_options["num_last_objects"]

    def get_max_graph_width(self):
        return self.summary_options["max_graph_width"]

    def get_exclude_from_total_time(self):
        return self.__validate_list(self.summary_options["exclude_from_total_time"])

    def get_exclude_from_entry_time_distribution(self):
        return self.__validate_list(
            self.summary_options["exclude_from_entry_time_distribution"]
        )

    def get_project_areas(self):
        return self.__validate_list(self.project_areas)

    def get_projects(self):
        return self.__validate_list(self.projects)

    def get_general_areas(self):
        return self.__validate_list(self.general_areas)

    def get_areas(self):
        return {**self.project_areas, **self.general_areas}

    def get_area(self, area):
        areas = self.get_areas()
        if area in areas:
            return areas[area]

        else:
            return {
                "name": area,
                "rendering_string": self.DEFAULT_RENDERING,
                "use_last_objects": False,
            }

    def get_object_name(self, area, obj):
        if area in self.project_areas:
            if obj in self.projects:
                return self.get_project_name(obj)

        return obj

    def get_project_name(self, obj):
        if obj in self.projects:
            return self.projects[obj].get("name", obj)

        return obj

    def get_project_description(self, obj):
        if obj in self.projects:
            desc = "{0} :: {1}".format(
                self.projects[obj].get("name", obj),
                self.projects[obj].get("desc", "no description"),
            )
            if "link" in self.projects[obj]:
                desc += " ({})".format(self.projects[obj]["link"])
            return desc

        return None

    def __validate_list(self, config_list):
        if config_list is None:
            return []

        else:
            return config_list

    def __validate_dict(self, config_dict):
        if config_dict is None:
            return {}

        else:
            return config_dict
