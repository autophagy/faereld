# -*- coding: utf-8 -*-

"""
faereld.models
--------------

"""

from wisdomhord import Bisen, Sweor, String, Wending, DateTime

class FaereldWendingEntry(Bisen):

  __invoker__ = 'Færeld'
  __description__ = 'Productive task time tracking data produced by Færeld'

  col1 = Sweor('AREA',   String)
  col2 = Sweor('OBJECT', String)
  col3 = Sweor('START',  Wending)
  col4 = Sweor('END',    Wending)


class FaereldDatetimeEntry(Bisen):

  __invoker__ = 'Færeld'
  __description__ = 'Productive task time tracking data produced by Færeld'

  col1 = Sweor('AREA',   String)
  col2 = Sweor('OBJECT', String)
  col3 = Sweor('START',  DateTime)
  col4 = Sweor('END',    DateTime)
