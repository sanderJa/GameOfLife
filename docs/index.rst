.. GameOfLife documentation master file, created by
   sphinx-quickstart on Tue Jun 10 19:12:52 2025.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

GameOfLife documentation
========================


Projekt "Game of Life" to gra symulacyjna oparta na automacie komórkowym zaproponowanym przez Johna Conwaya. Aplikacja została napisana w języku Python z wykorzystaniem biblioteki Tkinter do tworzenia graficznego interfejsu użytkownika.

Funkcje projektu:
-----------------
- Interfejs graficzny z siatką komórek, które można aktywować kliknięciem myszki.
- Obsługa podstawowych zasad gry (np. narodziny, śmierć i przetrwanie komórek).
- Możliwość definiowania własnych reguł gry.
- Zapisywanie i wczytywanie szablonów z katalogu `resources/templates`.
- Okno startowe umożliwiające wybór ustawień gry.
- Osobne okno do podglądu i wyboru zapisanych szablonów.
- Możliwość pauzowania i wznawiania symulacji.
- Czysty podział logiki gry i interfejsu użytkownika.

Struktura katalogów:
--------------------
- `logic/` – logika gry (np. zarządzanie siatką i regułami).
- `gui/` – interfejs graficzny użytkownika.
- `resources/templates/` – zapisane szablony wzorów początkowych.
- `main.py` – punkt wejścia do aplikacji.

Wymagania:
----------
- Python 3.9 lub nowszy
- Biblioteka standardowa (Tkinter)

Instrukcja uruchomienia:
------------------------
Aby uruchomić aplikację, wykonaj w terminalu:

.. code-block:: bash

   python main.py

---


.. toctree::
   :maxdepth: 4
   :caption: Contents:

   GameOfLife
