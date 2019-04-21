# -*- coding: utf-8 -*-


class Defaults:

    # Default Configuration Options
    DEFAULT_DATA_OPTIONS = {
        "data_path": "~/.andgeloman/faereld/faereld.hord",
        "use_wending": False,
        "num_last_objects": 5,
    }

    # Default Project Areas
    DEFAULT_RENDERING = (
        "On {date} I worked on {object} ({area_name}) for {duration} - {purpose}"
    )
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
