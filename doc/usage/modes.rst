=====
Modes
=====

Færeld has 3 usage modes: ``summary``, ``insert`` and ``sync``.

Summary Mode
============

Summary mode can be used via:

.. code-block:: bash

    $ faereld summary

Summary mode will print several summaries of the available Færeld data
including:

- Summary of total days, entries and hours logged.
- Bar graph of total time logged per area.
- Box plot diagram of entry time distribution per area (except ``IRL``).
- The last 10 entries logged.


Insert Mode
===========

Insert mode can be used via:

.. code-block:: bash

    $ faereld insert

Færeld will first ask you to choose the area that the current task belongs to.
For a list of areas and their explainations, see the :doc:`areas` documentation.

.. code-block:: bash

    [ Areas :: RES // DES // DEV // DOC // TST // IRL // RDG // LNG ]
    Area :: DEV

If the chosen area is a project specific one (``RES``, ``DES``, ``DEV``, ``DOC``
or ``TST``) then you will be asked to enter the project that this task belongs
to. These projects can be defined in the :doc:`configuration`.

.. code-block:: bash

    [ Objects :: faereld // insegel // datarum // aerende // antimber // hraew ]
    Object :: faereld

If the area is a non-project specific one, then you will be prompted to just
fill out the name of whatever the task is.

You will then be asked to enter the start and end datetime of the task. This
task must be in form ``Day Short-Month Year // 24H.M``. For example, a task
beginning on the 3rd of December 2017 at 10pm should be entered as::

    From :: 03 Dec 2017 // 22.00

Similar rules apply if using Wending mode dates, which are disabled by default.

Sync Mode
=========

Sync mode can be used via:

.. code-block:: bash

    $ faereld sync

    Batch (01 / 01) :: 24 entries synced to Hrǽw

Sync mode will POST any unsynced Færeld entries as JSON data to an endpoint.
The endpoint to sync to as API key used for authentication can be defined in
the :doc:`configuration`.

.. note:: Sync mode is currently not implemented.
