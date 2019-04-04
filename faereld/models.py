# -*- coding: utf-8 -*-
"""
faereld.models
--------------

This module models the data structure used within faereld, which consists of:
AREA    :: The category of the time tracked
OBJECT  :: The specific object or project tracked
START   :: The datetime the task was started
END     :: The datetime the task was finished
PURPOSE :: The purpose of the task, if a project task.

The START and END fields can either use the Gregorian datetime (by default),
which returns the standard python datetime object. Or it can use the Wending
datetime, which returns a Wending object as defined in Datarum.
"""

from wisdomhord import Bisen, DateTime, String, Sweor, Wending


class FaereldWendingEntry(Bisen):
    __invoker__ = "Færeld"
    __description__ = "Productive task time tracking data produced by Færeld"
    area = Sweor("AREA", String)
    obj = Sweor("OBJECT", String)
    start = Sweor("START", Wending)
    end = Sweor("END", Wending)
    purpose = Sweor("PURPOSE", String)


class FaereldDatetimeEntry(Bisen):
    __invoker__ = "Færeld"
    __description__ = "Productive task time tracking data produced by Færeld"
    area = Sweor("AREA", String)
    obj = Sweor("OBJECT", String)
    start = Sweor("START", DateTime)
    end = Sweor("END", DateTime)
    purpose = Sweor("PURPOSE", String)
