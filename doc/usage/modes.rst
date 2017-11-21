=====
Modes
=====

Færeld has 3 usage modes: ``summary``, ``insert`` and ``sync``.

Summary Mode
============

Summary mode can be used via:

.. code-block:: bash

    $ faereld summary

    FÆRELD :: SUMMARY MODE
    153 DAYS // 425 ENTRIES // TOTAL 17h05m

    RES [1h0m]  | ||||||||||
    DES [1h20m] | ||||||||||||||||
    DEV [3h30m] | ||||||||||||||||||||||||||||||||||||
    DOC [0h45m] | |||||||
    TST [0h30m] | |||||
    IRL [2h0m]  | |||||||||||||||||||||||||
    RDG [4h30m] | ||||||||||||||||||||||||||||||||||||||||||||||||||
    LNG [2h10m] | |||||||||||||||||||||||||||||
    BKG [1h20m] | ||||||||||||||||

    MIN 0h14m // MAX 2h41m // AVG 1h20

    LAST 10 ENTRIES
    On 2 Forst 226 I worked on Færeld (Development) for 0h22m
    On 2 Forst 226 I was at Edible Alchemy Ginger Beer Workshop for 1h30m
    On 1 Forst 226 I read Jorge Luis Borges' Fictions for 0h25m
    On 1 Forst 226 I studied German for 0h30m
    On 1 Forst 226 I worked on Færeld (Documentation) for 0h12m
    On 1 Forst 226 I worked on Datárum (Documentation) for 0h58m
    On 30 Mist 226 I worked on Færeld (Documentation) for 0h15m
    On 30 Mist 226 I worked on Færeld (Development) for 0h15m
    On 30 Mist 226 I worked on Færeld (Documentation) for 0h40m
    On 30 Mist 226 I worked on Færeld (Development) for 0h20m

This produces a summary of recorded entries that includes the number of days
and entries recorded, as well as the amount recorded for each type of task.

Insert Mode
===========

Insert mode can be used via:

.. code-block:: bash

    $ faereld insert

    FÆRELD :: INSERT MODE
    153 DAYS // 425 ENTRIES // TOTAL 17h05m

    [ Areas :: RES // DES // DEV // DOC // TST // IRL // RDG // LNG ]
    Area :: DEV

    [ Objects :: faereld // insegel // datarum // aerende // antimber // hraew ]
    Object :: faereld

    From :: 30 mist 226 // 04.30
    To :: 30 mist 226 // 04.50

    On 30 Mist 226 I worked on Færeld (Development) for 0h20m
    Is this correct? (y/n) :: y
    Færeld entry added

Insert mode prompts the user to fill in information about the task being
performed. The valid areas are pre-defined, and map to :doc:`areas` I wish to
track. The valid objects for project based areas are defined in the
:doc:`configuration`.

Sync Mode
=========

Sync mode can be used via:

.. code-block:: bash

    $ faereld sync

    Batch (01 / 01) :: 24 entries synced to Hrǽw

This syncs any unsynced entries to the Hrǽw database, which can then be used for
visualisation. The endpoint to sync to as API key used for authentication can
be defined in the :doc:`configuration`.

.. note:: Sync mode is currently not implemented.
