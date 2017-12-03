# -*- coding: utf-8 -*-

"""
faereld.configuration
------------------

"""

from os import path, makedirs
import yaml


class Configuration(object):

    # Default Configuration Options

    DEFAULT_DATA_OPTIONS = {
        'data_options': '~/.andgeloman/faereld/data.db',
        'use_wending': False
    }

    # Default Sync Options

    DEFAULT_SYNC_OPTIONS = {
        'endpoint': None,
        'api_key': None,
        'batch_size': 50
    }

    # Default Projects

    DEFAULT_PROJECTS = {
        'faereld': {
            'name': 'Færeld',
            'link': 'https://github.com/Autophagy/faereld'
        }
    }

    DEFAULT_CONFIG = {
        'data_options': DEFAULT_DATA_OPTIONS,
        'sync_options': DEFAULT_SYNC_OPTIONS,
        'projects': DEFAULT_PROJECTS
    }

    # Banner to prepend to the default configuration if it does not exist.

    CONFIG_BANNER = """# Færeld :: Configuration File
#
# Please see
# https://faereld.readthedocs.io/en/latest/usage/configuration.html for a
# complete reference of configuration options, as well as their effects.

"""

    def __init__(self, configuration_path):
        """ On initialisation, preload the configuration options from the
        defaults.
        """
        self.data_options = self.DEFAULT_DATA_OPTIONS
        self.sync_options = self.DEFAULT_SYNC_OPTIONS
        self.projects = self.DEFAULT_PROJECTS
        self.__load_configuration(configuration_path)

    def __load_configuration(self, configuration_path):
        """ Load the configuration from the supplied path. If the file does
        not exist at this path, create it from the default config settings.
        """
        expanded_path = path.expanduser(configuration_path)
        if not path.exists(path.dirname(expanded_path)):
            makedirs(path.dirname(expanded_path))

        if not path.exists(expanded_path):
            with open(expanded_path, 'w') as config_file:
                config_file.write(self.CONFIG_BANNER)
                yaml.dump(self.DEFAULT_CONFIG, config_file,
                          default_flow_style=False, allow_unicode=True)
            self.data_options = self.DEFAULT_DATA_OPTIONS
            self.sync_options = self.DEFAULT_SYNC_OPTIONS
            self.projects = self.DEFAULT_PROJECTS
        else:
            self.__load_configuration_values(expanded_path)

    def __load_configuration_values(self, path):
        """ Load the configuration file, update the config values from this
        file.
        """
        with open(path, 'r') as config_file:
            config_dict = yaml.load(config_file)

            config_variables = {
                'data_options': self.data_options,
                'sync_options': self.sync_options,
                'projects': self.projects
            }

            for key, value in config_variables.items():
                self.__update_configuration(key, config_dict, value)

    def __update_configuration(self, config_key, config_dict, var):
        """ Update a config dictionary given a category key
        """
        if config_key in config_dict:
            var.update(config_dict[config_key])

    def get_data_path(self):
        return self.data_options['data_path']

    def get_use_wending(self):
        return self.data_options['use_wending']

    def get_sync_options(self):
        return self.sync_options

    def get_projects(self):
        return self.projects
