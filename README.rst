

Configuration
=============

Configure API keys
------------------

Die Funktionsweise und das Erstellen von GEVER API Keys ist in der
[GEVER Dokumentation](https://docs.onegovgever.ch/dev-manual/api/authentication/oauth2_token_auth/)
beschrieben.

Die generierten Service-Keys der verschiedenen GEVER-Installationen werden in einen
Ordner kopiert (Namenskonvention: ``keys``).
Dieser Ordner wird über die Umgebungsvariabel ``OPENGEVER_APICLIENT_KEY_DIRS``
konfiguriert. Mehrere Ordner können mit dem Trennzeichen ``:`` getrennt werden.


Umgebungsvariabeln
------------------

``OPENGEVER_APICLIENT_KEY_DIRS``
  Pfadliste zu Keys Ordnern getrennt mit ``:``.

``OPENGEVER_APICLIENT_USER_AGENT``
  Zusätzlicher User-Agent (z.B. ``MeineApp/3.5``).


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

Make sure that the GEVER testserver is running before running the tests (`bin/testserver`).

.. code::

   source venv/bin/activate
   pytest
