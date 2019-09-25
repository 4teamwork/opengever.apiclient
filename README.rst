Ziele
=====

* Versionierung von GEVER behandeln

    * Dies ist der wichtigste Grund für die Entstehung dieses Pakets. Der `opengever.apiclient` kann in einer bestimmten Version installiert werden und retourniert unabhängig von der GEVER Version konstistente Daten.
    * Die Art der Implementierung der Versionierung ist noch nicht entschieden.

* Dokumentation über Verwendung

    * Sämtliche Zugriffe auf die GEVER API - auch sehr projekt-spezifische - müssen über dieses Paket abgehandelt werden. Dies, damit das GEVER Team die Art der Verwendung abschätzen kann.

    * DRY: Features wie Paginierung und Fehlerbehandlung werden nur ein Mal implementiert.

* Zusammenarbeit zwischen GEVER und django Team verbessern

    * Durch die Zusammenarbeit soll für das GEVER Team die Verwendung der API transparent werden. Das django Team erhält Feedback wenn die API nicht optimal angesprochen wird.


Aufbau
======

Organisation
------------

* Das django Team hat die Verantwortung für die Entwicklung dieses Pakets.
* Je eine Person aus dem GEVER und django Team muss die PRs reviewen.


Technisches
-----------

* Sämtliche requests müssen von diesem Paket behandelt werden.
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
Dieser Ordner wird über die Umgebungsvariabel ``OPENGEVER_APICLIENT_KEY_DIRS``
konfiguriert. Mehrere Ordner können mit dem Trennzeichen ``:`` getrennt werden.


Umgebungsvariabeln
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
