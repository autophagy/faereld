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
