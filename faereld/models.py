# -*- coding: utf-8 -*-

"""
faereld.models
--------------

"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, DateTime, Boolean

Base = declarative_base()

class FaereldEntry(Base):

    __tablename__ = 'faereld_entries'

    id          =   Column(Integer, primary_key=True)
    area        =   Column(String(3), nullable=False)
    object      =   Column(String(32), nullable=False)
    link        =   Column(String(200))
    start       =   Column(DateTime, nullable=False)
    end         =   Column(DateTime, nullable=False)
    synced      =   Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        repr = "<Feareld Entry :: {0} ({1} {2}) // {3} - {4} // Synced :: {5}"
        return repr.format(self.object,
                           self.area,
                           self.link,
                           self.start,
                           self.end,
                           self.synced)
