Configuration
=============

.. _configuration:

The configuration file for Færeld is located in `~/.andgeloman/faereld/config.yml`.


Data Options
------------

================ ======================= =============================
Option           Description             Default
================ ======================= =============================
data_path        Path to note sqllite db ~/.andgeloman/faereld/data.db

use_wending      Use Wending date format
                 instead of Gregorian    False

num_last_objects The number of objects   5
                 return when adding a
                 non-project task.
================ ======================= =============================

Summary Options
---------------

==================================== ========================================================= =======
Option                               Description                                               Default
==================================== ========================================================= =======
max_graph_width                      The maximum character width that the summary graphs       100
                                     should display. Useful if running in a large terminal
                                     window.
exclude_from_total_time              List of areas to exclude from the total time graph in     - TSK
                                     summary mode.
exclude_from_entry_time_distribution List of areas to exclude from the entry time distribution - IRL
                                     graph in summary mode.
==================================== ========================================================= =======

Project Areas
-------------

Project area definitions should be of the form:

.. code-block:: yaml

  code:
    name: Area Name
    rendering_string: On {date} I worked on {object} ({area_name}) for {duration}

For example, the default **Development** area is defined as follows:

.. code-block:: yaml

  DEV:
    name: Development
    rendering_string: On {date} I worked on {object} ({area_name}) for {duration}

The ``rendering_string`` is used within Færeld to render an entry. The above
defition would render a 30 minute development task on 2nd Jan 2017 for Project A
as:

.. code-block:: none

  On 02 Jan 2017 I worked on Project A (Development) for 30m

To render the string diferently, change this configuration option. For example,
to generate the rendered string:

.. code-block:: none

  [02 Jan 2018] -- Development -> Project A (30m)

You would configure the ``rendering_string`` as:

.. code-block:: yaml

  rendering_string: [{date}] -- {area_name} -> {object} ({duration})

The valid substitution options for a project area's rendering string are:

- ``{area}`` :: The area code of the entry (e.g. DEV)
- ``{area_name}`` :: The name of the area of the entry (e.g. Development)
- ``{object}`` :: The name of the object of the entry (e.g. Project A)
- ``{date}`` :: The date of the start date of the entry (e.g. 02 Jan 2017)
- ``{duration}`` :: The duration of the entry (e.g. 30m)
- ``{start}`` :: The start time of the entry (e.g. 18:00)
- ``{end}`` :: The end time of the entry (e.g. 23:42)

Projects
--------

Projects are defined within the config.yml, but there are no defaults. A
project must be defined in the following way:

.. code-block:: yaml

    projects:
      hraew:
        desc: A project information & documentation engine.
        link: https://github.com/Autophagy/hraew
        name: Hrǽw
      scieldas:
        desc: A service to provide metadata badges for Open Source projects.
        link: https://github.com/Autophagy/scieldas
        name: Scieldas

General Areas
-------------

General rea definitions should be of the form:

.. code-block:: yaml

  code:
    name: Area Name
    rendering_string: On {date} I worked on {object} for {duration}

For example, the default **Reading** area is defined as follows:

.. code-block:: yaml

  RDG:
    name: Reading
    rendering_string: On {date} I read {object} for {duration}
    use_last_objects: true

The ``rendering_string`` is used within Færeld to render an entry. The above
defition would render a 30 minute reading task on 2nd Jan 2017 for Book A
as:

.. code-block:: none

  On 02 Jan 2017 I read Book A for 30m

To render the string diferently, change this configuration option. For example,
to generate the rendered string:

.. code-block:: none

  [02 Jan 2018] -- Reading -> Book A (30m)

You would configure the ``rendering_string`` as:

.. code-block:: yaml

  rendering_string: [{date}] -- {area_name} -> {object} ({duration})

The valid substitution options for a project area's rendering string are:

- ``{area}`` :: The area code of the entry (e.g. RDG)
- ``{area_name}`` :: The name of the area of the entry (e.g. Reading)
- ``{object}`` :: The name of the object of the entry (e.g. Book A)
- ``{date}`` :: The date of the start date of the entry (e.g. 02 Jan 2017)
- ``{duration}`` :: The duration of the entry (e.g. 30m)
- ``{start}`` :: The start time of the entry (e.g. 18:00)
- ``{end}`` :: The end time of the entry (e.g. 23:42)


The ``use_last_objects`` option defines that, upon insertion of that area,
whether the last x objects (x being the defined value in
``data_options: num_last_projects`` to be inserted into that area are printed.
These can then be used as short hand when inserting an entry. For example, on
inserting a **Reading** task:

.. code-block :: none

  [ Areas :: RES // DES // DEV // DOC // TST // IRL // RDG // LNG // TSK ]
  Area :: RDG

  Last 5 RDG Objects ::
  [0] Italo Calvino's Our Ancestors
  [1] Iain M. Banks' Look to Windward
  [2] David Peak's The Spectacle of the Void
  [3] Benjamin H. Bratton's The Stack: On Software and Sovereignty
  [4] Herman Meville's Moby Dick
  Object :: [0]

In this example, selecting ``[0]`` as the object would then insert
``Italo Calvino's Our Ancestors`` into Færeld.
