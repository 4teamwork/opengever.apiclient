

Development
===========

Installation
------------

Installing the ``opengever.apiclient``:

.. code::

    pyenv shell 3.7.2
    python -m venv venv
    source venv/bin/activate
    pip install -e ".[tests]"


Installing a GEVER testserver:

.. code::

   pyenv shell 2.7.15
   ln -s development.cfg buildout.cfg
   python bootstrap.py
   bin/buildout


Run Tests
---------

.. code::

   source venv/bin/activate
   pytest
