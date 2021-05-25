Ziele
=====

* Breaking Changes der GEVER API behandeln

    * Dies ist der wichtigste Grund für die Entstehung dieses Pakets. Der `opengever.apiclient` kann in einer bestimmten Version installiert werden und retourniert unabhängig von der GEVER Version konsistente Daten.
    * Durch Kapselung der GEVER API die Fachanwendung vor Änderungen schützen. Basis: https://plonerestapi.readthedocs.io/en/latest/upgrade-guide.html
    * Die Art der Implementierung der Versionierung ist noch nicht entschieden.

* "Quality of Life" für die Entwickler

    * DRY: Features wie Paginierung und Fehlerbehandlung werden nur ein Mal implementiert.
    * Struktur: Auf endpoints der GEVER API operieren.
    * Unnamed endpoints: Models beibehalten https://plonerestapi.readthedocs.io/en/latest/content.html

* Zusammenarbeit zwischen GEVER und django Team verbessern

    * Das GEVER-Team führt Code Reviews der Pull Requests nur nach Bedarf durch, steht aber beratend zur Verfügung bei strukturellen Änderungen.


Aufbau
======

Organisation
------------

* @jone hat die Verantwortung für die Entwicklung dieses Pakets
* Die aktuelle Version wird für das Projekt `vertragsmanagement` entwickelt, es ist nicht die Erwartung, dass dieses Paket innerhalb von dem Projekt sauber entwickelt wird. Innerhalb von diesem Projekt hat das django-Team die Verantwortung für die Entwicklung. Jone wird die zweite Version entwickeln und auf eine saubere Basis stellen.

Technisches
-----------

* Sämtliche Requests müssen von diesem Paket behandelt werden.
* Die Objekte im Ordner `apiclient/models` repräsentieren GEVER-Inhaltstypen (https://docs.onegovgever.ch/dev-manual/api/content_types/)


Konfiguration
=============

API Keys konfigurieren
----------------------

Die Funktionsweise und das Erstellen von GEVER API Keys ist in der
[GEVER Dokumentation](https://docs.onegovgever.ch/dev-manual/api/authentication/oauth2_token_auth/)
beschrieben.

Die generierten Service-Keys der verschiedenen GEVER-Installationen werden in einen
Ordner kopiert (Namenskonvention: ``keys``).
Dieser Ordner wird über die Umgebungsvariable ``OPENGEVER_APICLIENT_KEY_DIRS``
konfiguriert. Mehrere Ordner können mit dem Trennzeichen ``:`` getrennt werden.


Umgebungsvariablen
------------------

``OPENGEVER_APICLIENT_KEY_DIRS``
  Pfadliste zu Keys Ordnern getrennt mit ``:``.

``OPENGEVER_APICLIENT_USER_AGENT``
  Zusätzlicher User-Agent (z.B. ``MeineApp/3.5``).


Entwicklung
===========

Installation
------------

Installation des ``opengever.apiclient``:

.. code::

    pyenv shell 3.7.2
    python -m venv venv
    source venv/bin/activate
    pip install -e ".[tests]"


Installation des GEVER Testservers:

.. code::

   pyenv shell 2.7.15
   ln -s development.cfg buildout.cfg
   python bootstrap.py
   bin/buildout


Tests ausführen
---------------

.. code::

   source venv/bin/activate
   pytest
