=====
Modes
=====

Færeld has 3 usage modes: ``summary``, ``insert`` and ``sync``.

Summary Mode
============

Summary mode can be used via:

.. code-block:: bash

    $ faereld summary

    Days 153 // Entries 234

    RES [1h0m]  | //////////
    DES [1h20m] | ////////////////
    DEV [3h30m] | ////////////////////////////////////
    DOC [0h45m] | ///////
    TST [0h30m] | /////
    RDG [4h30m] | //////////////////////////////////////////////////
    BKG [1h20m] | ////////////////

This produces a summary of recorded entries that includes the number of days
and entries recorded, as well as the amount recorded for each type of task.

Insert Mode
===========

Insert mode can be used via:

.. code-block:: bash

    $ faereld insert

    (Valid Areas :: RES // DES // DEV // DOC // TST // RDG // BKG)
    Area :: DOC

    (Valid Objects :: aerende // antimber // faereld // hraew // insegel)
    Object :: aerende

    From :: 24 Mist 226 // 12:00
    To :: 24 Mist 226 // 13:30

    On 24 Mist 226 I worked on Ærende (documentation) for 1h30m
    Is this correct? :: y

    Entry added.

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

The syncs any unsynced entries to the Hrǽw database, which can then be used for
visualisation. The endpoint to sync to as well as the username and password
used for authentication can be defined in the :doc:`configuration`.


