# RoboSim: vereinfachte Code-Dokumentation

## 1. Was macht RoboSim?

RoboSim simuliert einen Roboter mit zwei einzeln angetriebenen Rädern. In der
Web-Demo kann man ihn per Tastatur steuern oder einem Regler überlassen, der
einem geschlossenen Rundkurs folgt. Der Kurs ist über Breite, Höhe und
Kurvenstärke einstellbar. Die Oberfläche zeigt den Roboter, den Kurs, den
Bewegungsverlauf und den Abstand zur Linie. Neben der 2D-Ansicht gibt es eine
mit der Maus dreh- und zoombare 3D-Ansicht desselben Roboters und Rundkurses;
der Bewegungsverlauf erscheint in 2D.

Die Simulation ist ein Lernbeispiel, keine detaillierte physikalische
Simulation: Der Rundkursregler kennt die Roboterposition und den Kurs direkt.
Simulierte Liniensensoren gibt es noch nicht.

## 2. Aufbau

Der Code orientiert sich an einer **hexagonalen Architektur**. Die Grundidee:
Die Simulation soll unabhängig von einer konkreten Oberfläche funktionieren.
Sie kommuniziert über Schnittstellen, sogenannte **Ports**, mit austauschbaren
Bausteinen, den **Adaptern**.

```text
Tastatur ──> Tastaturadapter ──> Simulationsservice ──> Robotermodell
                                      │
                                      ├──> Regler ──> Rundkurs
                                      │
                                      └──> Anzeige ──> Browser
```

Die Pfeile zeigen hier vereinfacht, wer wen aufruft. Die Weboberfläche verbindet
die Bausteine und startet die Simulationsschritte. Das [vereinfachte
PlantUML-Klassendiagramm](./architektur.puml) liegt daneben. Es kann mit einer
PlantUML-Vorschau geöffnet werden; die Textübersicht oben funktioniert auch
ohne Zusatzprogramm.

### Die wichtigsten Dateien

| Datei | Aufgabe |
|---|---|
| [robot.py](../src/domain/robot.py) | Enthält Roboterzustand, Radgeschwindigkeiten und das Bewegungsmodell. |
| [track.py](../src/domain/track.py) | Erzeugt den Rundkurs und berechnet Punkte und Abstände. |
| [ports.py](../src/application/ports.py) | Beschreibt die Schnittstellen für Simulation, Regler und Anzeige. |
| [simulation.py](../src/application/simulation.py) | Verbindet Roboter, optionalen Regler und Anzeige für jeden Simulationsschritt. |
| [keyboard_control.py](../src/adapters/keyboard_control.py) | Übersetzt Tasteneingaben in Radgeschwindigkeiten. |
| [line_follower.py](../src/adapters/line_follower.py) | Enthält Regler für den Rundkurs und die gerade Konsolen-Demo. |
| [nicegui_view.py](../src/adapters/nicegui_view.py) | Zeichnet Roboter und Kurs in der Weboberfläche. |
| [console_view.py](../src/adapters/console_view.py) | Gibt den Roboterzustand auf der Konsole aus. |
| [web_demo.py](../src/web_demo.py) | Baut die Web-Demo zusammen und verarbeitet deren Bedienelemente. |
| [main.py](../src/main.py) und [line_follower_demo.py](../src/line_follower_demo.py) | Starten einfache Konsolenbeispiele. |

Die Ports legen fest, welche Methoden ein Baustein anbieten muss. Der
Simulationsservice nutzt zum Beispiel `ControllerPort`, um einen Regler nach
Radgeschwindigkeiten zu fragen, und `RobotViewPort`, um einen neuen Zustand
anzuzeigen. Die Web-Demo wählt den Regler derzeit direkt am
`SimulationService` aus.

## 3. Ablauf eines Simulationsschritts

1. Nach dem Start ruft ein Timer in der Web-Demo ungefähr alle 0,05 Sekunden
   `simulation.step(0.05)` auf.
2. Ist der Regler aktiv, berechnet er aus dem aktuellen Zustand neue
   Radgeschwindigkeiten. Im manuellen Modus kommen diese vom Tastaturadapter.
3. Der Simulationsservice übergibt die Geschwindigkeiten und die Schrittweite
   an das Robotermodell.
4. Das Robotermodell berechnet die neue Position und Ausrichtung.
5. Der Simulationsservice übergibt den neuen Zustand an die Anzeige. Diese
   aktualisiert die Zeichnung und den Abstand zum Kurs.

Der Timer bestimmt, wann ein Schritt ausgelöst wird. Jeder Schritt verwendet
die feste **simulierte** Zeit von 0,05 Sekunden; die tatsächliche
Ausführungsgeschwindigkeit kann davon abweichen.

## 4. Roboter und Bewegung

`RobotState` enthält die Position `x`, `y` und die Ausrichtung `heading` im
Bogenmaß. `WheelSpeeds` enthält die Geschwindigkeit des linken und rechten
Rads. Im Modell zeigen die positive x-Achse nach rechts und die positive
y-Achse nach oben. Der Winkel 0 zeigt entlang der positiven x-Achse;
positive Winkel drehen gegen den Uhrzeigersinn.

Das Modell berechnet aus den Radgeschwindigkeiten:

- **Vorwärtsgeschwindigkeit:** Mittelwert der beiden Radgeschwindigkeiten.
- **Drehgeschwindigkeit:** Differenz der Radgeschwindigkeiten geteilt durch
  den Radabstand.

Gleiche Geschwindigkeiten ergeben eine Geradeausfahrt, unterschiedliche
Geschwindigkeiten eine Drehung. Position und Winkel werden in kleinen
Zeitschritten näherungsweise aktualisiert.

## 5. Rundkurs und Regler

Der Rundkurs wird mit einer parametrischen Formel erzeugt. Breite und Höhe
skalieren die Form, die Kurvenstärke verändert ihre Wölbungen. Aus der Formel
werden 360 Punkte erzeugt und zu einer geschlossenen Linie verbunden. Diese
Näherung wird für Zeichnung, Abstandsmessung und Regelung verwendet.

Bei jedem Schritt sucht der Rundkursregler den nächstgelegenen Punkt auf der
Linie und einen Zielpunkt etwas weiter in Fahrtrichtung. Er vergleicht die
Richtung zum Ziel mit der aktuellen Ausrichtung und berechnet daraus die
Radgeschwindigkeiten. So lenkt der Roboter entlang des Kurses.

## 6. Bedienung und Tests

Die Start- und Installationsanleitung steht in der
[README im Projektordner](../README.md). Kurzfassung vom Projektordner aus:

```text
python -m pip install -r requirements.txt
python -m src.web_demo
```

Die Anwendung ist anschließend unter `http://127.0.0.1:8093` erreichbar.
Mit **Kurs übernehmen / Zurücksetzen** werden die gewählten Kursparameter
übernommen und die Simulation zurückgesetzt. **Manuell** aktiviert W/A/S/D;
**Linienfolger** aktiviert den Regler. Start und Pause steuern den Ablauf.

Die Tests im [Tests-Ordner](../tests) prüfen unter anderem Bewegung,
Reglerwechsel, Rundkurs und Darstellung:

```text
python -m unittest discover -s tests
```

## 7. Statische Browser-Version mit Pyodide

Die Pages-Version liegt in `site/`. Ihre HTML-/CSS-/JavaScript-Oberfläche ruft
die Python-Schnittstelle in [browser_api.py](../src/browser_api.py) auf. Der
Build-Helfer [build_pages.py](../scripts/build_pages.py) kopiert die benötigten
Python-Module unverändert in das statische Ausgabe-Verzeichnis. Pyodide lädt
diese Dateien in seine Browser-Laufzeit; `browser_api.py` verbindet sie mit
dem Simulationsservice und liefert Zustand sowie Kurs als JSON zurück.

Die Oberfläche zeichnet den Kurs, Roboter und Bewegungsverlauf als SVG. Die
NiceGUI-Ansicht und ihre 3D-Szene werden nicht verwendet. Die lokale NiceGUI-App
bleibt separat unter `python -m src.web_demo` verfügbar.

Der GitHub-Actions-Workflow erzeugt beim Deployment ein statisches Site-Artefakt
aus `site/` und den Python-Modulen. Lokal lässt es sich mit diesen Befehlen
erzeugen und testen:

```text
python scripts/build_pages.py
python -m http.server 8000 --directory build/pages
```

Der Workflow veröffentlicht bei Pushes auf den Branch `pyodide`. Die
veröffentlichte Website benötigt beim ersten Aufruf Netzwerkzugriff auf das
Pyodide-CDN. Pages muss in den Repository-Einstellungen als Deployment-Quelle
**GitHub Actions** verwenden.
