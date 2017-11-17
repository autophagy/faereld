Configuration
=============

.. _configuration:

The configuration file for Færeld is located in `~/.andgeloman/faereld/config.yml`.


Data Path Options
-----------------

========= ======================= =============================
Option    Description                Default
========= ======================= =============================
data_path Path to note sqllite db ~/.andgeloman/faereld/data.db
========= ======================= =============================

Sync Options
------------

========== ======================================================== =======
Option     Description                                              Default
========== ======================================================== =======
endpoint   The HTTP endpoint to post Færeld data to.
api_key    API key to use to authenticate with the endpoint.
batch_size The number of entries to post to the endpoint at a time. 50
========== ======================================================== =======

Projects
--------

========== ======================================================== =======
Option     Description                                              Default
========== ======================================================== =======
projects   Array of Project codes, names and links. See below.
========== ======================================================== =======

Projects are defined within the config.yml, but there are no defaults. A
project must be defined in the following way:

.. code-block:: yaml

    projects:
      aerende:
        name: Ærende
        link: https://github.com/Autophagy/aerende
      hraew:
        name: Hrǽw
        link: https://github.com/Autophagy/hraew