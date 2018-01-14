======
Færeld
======

.. image:: http://scieldas.autophagy.io/rtd/faereld.png
    :target: http://faereld.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: http://scieldas.autophagy.io/licenses/MIT.png
   :target: LICENSE
   :alt: MIT License

Færeld is a tool to facilitate time tracking of what I'm working on.
Goal is to then visualise this data in Hrǽw and use that to examine and
optimise what I spend my time on.

Documentation is available on `ReadTheDocs`_.

.. image:: seonu/_static/faereld.png
    :alt: faereld-screenshot
    :align: center

Installation
============

Færeld requires python >= 3.6.

Via The Repo
-------------

To install Færeld from the repo, you can clone it and set up a clean environment
with ``virtualenv``: ::

    git clone git@github.com:Autophagy/faereld.git
    cd faereld
    virtualenv .venv -p python3.6
    source .venv/bin/activate

Then, install the package: ::

    pip install --user -e .

You can now run Færeld via ``faereld insert``.


.. _ReadTheDocs: https://faereld.readthedocs.io/en/latest/
