# -*- coding: utf-8 -*-

"""
faereld.controller
------------------

"""

from . import models
from os import path
import sqlalchemy

class Controller(object):

    def __init__(self, config):
        self.config = config
        self.data_path = path.expanduser(self.config.get_data_path())
        self.session = self.create_session(self.data_path)

    # [ Filesystem Reading / Writing ]

    def create_session(self, data_path):
        engine = sqlalchemy.create_engine('sqlite:///{0}'.format(data_path))
        models.FaereldEntry.metadata.create_all(engine)
        return sqlalchemy.orm.sessionmaker(bind=engine)()

