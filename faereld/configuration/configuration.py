# -*- coding: utf-8 -*-

from collections import OrderedDict
from os import makedirs, path
from typing import Dict, List

import yaml
from faereld.printer import Highlight, Printer

from .defaults import Defaults


class Configuration(object):
    def __init__(self, configuration_path):
        """ On initialisation, preload the configuration options from the
        defaults.
        """
        self.data_options = Defaults.DEFAULT_DATA_OPTIONS
        self.configured_project_areas = Defaults.DEFAULT_PROJECT_AREAS
        self.configured_projects = Defaults.DEFAULT_PROJECTS
        self.general_areas = Defaults.DEFAULT_GENERAL_AREAS
        self.summary_options = Defaults.DEFAULT_SUMMARY_OPTIONS
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
            self.__write_config_file(expanded_path, Defaults.DEFAULT_CONFIG)
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
            "project_areas": self.configured_project_areas,
            "projects": self.configured_projects,
            "general_areas": self.general_areas,
        }
        with open(path, "r") as config_file:
            config_dict = yaml.load(config_file, Loader=yaml.FullLoader)
            if config_dict is None:
                config_dict = {}
            for key, value in config_variables.items():
                self.__update_configuration(key, config_dict, value)
        self.__write_config_file(path, config_variables)

    def __update_configuration(self, config_key, config_dict, var):
        """ Update a config dictionary given a category key
        """
        if config_key in config_dict:
            if config_key in Defaults.MUST_BE_PRESENT_CONFIGS:
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
            config_file.write(Defaults.CONFIG_BANNER)
            for key, value in config.items():
                config_file.write(Defaults.CONFIG_AREA_HEADERS[key])
                config_file.write("\n")
                yaml.safe_dump(
                    {key: OrderedDict(value)},
                    config_file,
                    default_flow_style=False,
                    allow_unicode=True,
                )
                config_file.write("\n")

    @property
    def data_path(self) -> str:
        """ Returns the path to the Faereld data hord. """
        return self.data_options["data_path"]

    @property
    def use_wending(self) -> bool:
        """ Returns whether or not wending dates should be used. """
        return self.data_options["use_wending"]

    @property
    def num_last_objects(self) -> int:
        """ Returns how many of the previously referenced objects for that specific area should be returned
        as shorthand.
        """
        return self.data_options["num_last_objects"]

    @property
    def max_graph_width(self) -> int:
        """ Returns the maximum width in characters that a Faereldian graph should be. """
        return self.summary_options["max_graph_width"]

    @property
    def exclude_from_total_time(self) -> List[str]:
        """ Returns a list of areas that should be excluded from the total time summary graph. """
        return self.__validate_list(self.summary_options["exclude_from_total_time"])

    @property
    def exclude_from_entry_time_distribution(self) -> List[str]:
        """ Returns a list of areas that should be excluded from the entry time distribution summary graph. """
        return self.__validate_list(
            self.summary_options["exclude_from_entry_time_distribution"]
        )

    @property
    def project_areas(self) -> List[str]:
        """ Returns the list of project-specific areas. """
        return self.__validate_list(self.configured_project_areas)

    @property
    def projects(self) -> List[str]:
        """ Returns the list of configured projects. """
        return self.__validate_list(self.configured_projects)

    @property
    def areas(self) -> Dict:
        """ Returns a dictionary of configured project and general areas, as well as their associated
        configurations.
        """
        return {**self.configured_project_areas, **self.general_areas}

    def get_area(self, area):
        return self.areas.get(
            area,
            {
                "name": area,
                "rendering_string": Defaults.DEFAULT_RENDERING,
                "use_last_objects": False,
            },
        )

    def get_object_name(self, area, obj):
        if area in self.configured_project_areas:
            if obj in self.configured_projects:
                return self.get_project_name(obj)

        return obj

    def get_project_name(self, obj):
        if obj in self.configured_projects:
            return self.configured_projects[obj].get("name", obj)

        return obj

    def get_project_description(self, obj):
        if obj in self.configured_projects:
            desc = "{0} :: {1}".format(
                self.configured_projects[obj].get("name", obj),
                self.configured_projects[obj].get("desc", "no description"),
            )
            if "link" in self.configured_projects[obj]:
                desc += " ({})".format(self.configured_projects[obj]["link"])
            return desc

        return None

    @staticmethod
    def __validate_list(config_list):
        if config_list is None:
            return []

        else:
            return config_list

    @staticmethod
    def __validate_dict(config_dict):
        if config_dict is None:
            return {}

        else:
            return config_dict
