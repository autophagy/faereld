# -*- coding: utf-8 -*-

"""
faereld.controller
------------------

"""

from . import models
from os import path
import sqlalchemy
import datarum
import datetime
import math

class Controller(object):

    project_areas = {
        'RES': 'Research',
        'DES': 'Design',
        'DEV': 'Development',
        'DOC': 'Documentation',
        'TST': 'Testing',
    }

    misc_areas = {
        'IRL': 'Real life engagements (confs/talks/meetups)',
        'RDG': 'Reading',
        'LNG': 'Languages',
        'BKG': 'Baking'
    }

    areas = project_areas.copy()
    areas.update(misc_areas)

    rendering_strings = {
        'projects': 'On {0} I worked on {1} ({2}) for {3}',
        'IRL': 'On {0} I was at {1} for {2}',
        'RDG': 'On {0} I read {1} for {2}',
        'LNG': 'On {0} I learned {1} for {2}',
        'BKG': 'On {0} I made {1} for {2}'
    }


    def __init__(self, config):
        self.config = config
        self.data_path = path.expanduser(self.config.get_data_path())
        self.session = self.create_session(self.data_path)

    # [ Filesystem Reading / Writing ]

    def create_session(self, data_path):
        engine = sqlalchemy.create_engine('sqlite:///{0}'.format(data_path))
        models.FaereldEntry.metadata.create_all(engine)
        return sqlalchemy.orm.sessionmaker(bind=engine)()


    # Summary Mode

    def summary(self):
        return True

    # Insert Mode

    def insert(self):
        print("\n[ Areas :: {0} ]".format(' // '.join(self.areas.keys())))
        area = input('Area :: ').upper()

        if area in self.project_areas:
            object, link = self._project_object()
        else:
            object, link = self._non_project_object()

        # Assume to be in the form [date // time]
        from_date = input('From :: ')
        wending_date, from_date_gregorian = self.convert_input_date(from_date)

        to_date = input('To :: ')
        _, to_date_gregorian = self.convert_input_date(to_date)

        time_diff = self._time_diff(from_date_gregorian, to_date_gregorian)

        if area in self.project_areas:
            project_name = self.config.get_projects()[object]['name']
            print(self.rendering_strings['projects'].format(wending_date.formatted(),
                                                       project_name,
                                                       self.areas[area],
                                                       time_diff))
        else:
            print(self.rendering_strings[area].format(wending_date.formatted(),
                                                 object,
                                                 time_diff))

    def _project_object(self):
        projects = self.config.get_projects()

        print("\n[ Objects :: {0} ]".format(' // '.join(projects.keys())))
        object = input('Object :: ')

        while object not in projects:
            print("\nInvalid Project :: {0}".format(object))
            object = input('Object :: ')

        link = projects[object]['link']
        return (object, link)

    def _non_project_object(self):
        object = input('Object :: ')

        return (object, None)

    def convert_input_date(self, date_string):
        date, time = date_string.split(' // ')
        wending_date = datarum.wending.from_date_string(date)
        gregorian_date = datarum.to_gregorian(wending_date)
        time = datetime.datetime.strptime(time, '%H.%M')

        return (wending_date,
                gregorian_date.replace(hour=time.hour, minute=time.minute))

    def _time_diff(self, from_date, to_date):
        diff_delta = to_date - from_date
        hours, remainder = divmod(diff_delta.seconds, 3600)
        minutes = math.floor(remainder/60)

        return "{0}h{1}m".format(hours, minutes)

    # Sync Mode

    def sync(self):
        print("Sync mode is currently not enabled.")
