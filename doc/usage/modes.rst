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

    Design :: 23 hours
    Development :: 57 hours
    Documentation :: 12 hours
    Reading :: 42 hours

This produces a summary of recorded entries that includes the number of days
and entries recorded, as well as the amount recorded for each type of task.

Insert Mode
===========

Insert mode can be used via:

.. code-block:: bash

    $ faereld insert

    Type :: project
    Project name :: aerende
    Task :: documentation
    From :: 24 Mist 226 // 12:00
    To :: 24 Mist 226 // 13:30

    Is this correct?
    On [24 Mist 226] I worked on [aerende (documentation) ] for [1 hour, 30 minutes]

    Entry added.

Insert mode prompts the user to fill in information about the task being 
performed.

Sync Mode
=========

Sync mode can be used via:

.. code-block:: bash

    $ faereld sync

    Batch (01 / 01) :: 24 entries synced to Hrǽw

The syncs any unsynced entries to the Hrǽw database, which can then be used for
visualisation. The endpoint to sync to as well as the username and password
used for authentication can be defined in the :doc:`configuration`.


