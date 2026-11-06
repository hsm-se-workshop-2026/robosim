# Einfacher Architekturentwurf

Eine vereinfachte Erklärung des Codes und der Architektur steht in der
[Code-Dokumentation](../documentation/code-dokumentation.md).

Der Entwurf zeigt eine hexagonale Architektur als kleinen Python-Monolithen.
Der Simulationskern kennt weder Tastatur noch Benutzeroberfläche.

```text
Tastaturadapter oder Regler
           |
           v
Eingangsport (SimulationInputPort)
           |
           v
Simulationsservice -------> Robotermodell
      |       ^
      |       | Robotenzustand
      |   ControllerPort
      v
Ausgangsport (RobotViewPort)
           |
           v
Konsolenadapter
```

## Ordner

- `domain/robot.py`: Roboterzustand und Bewegung des Differentialantriebs.
- `domain/track.py`: parametrischer Rundkurs und Abstand zum Kurs.
- `application/ports.py`: Schnittstellen zwischen Kern und Adaptern.
- `application/simulation.py`: Anwendungslogik; implementiert den Eingangsport und verwendet bei Bedarf einen Regler.
- `adapters/keyboard_control.py`: übersetzt Tasten in Radgeschwindigkeiten.
- `adapters/line_follower.py`: Regler für den Rundkurs und für die gerade Konsolen-Demo.
- `adapters/console_view.py`: gibt den Zustand aus.
- `adapters/nicegui_view.py`: zeigt Roboter und Linie in 2D und 3D sowie den Bewegungsverlauf in 2D.
- `main.py`: verbindet die Bausteine und startet ein kleines Beispiel.
- `web_demo.py`: verbindet die Bausteine für die grafische Linienfolger-Demo.

## Ausprobieren

Vom Projektordner aus:

```text
python -m src.main
```

Die Linienfolger-Demo startet den Roboter neben einer geraden Linie und gibt
seine Bewegung in der Konsole aus:

```text
python -m src.line_follower_demo
```

Für die grafische Demo wird NiceGUI benötigt. Falls noch nicht installiert:

```text
python -m pip install -r requirements.txt
```

Danach die Demo starten:

```text
python -m src.web_demo
```

Im Browser `http://127.0.0.1:8093` öffnen und **Start / Fortsetzen** wählen.
Der rote Kreis stellt den Roboterkörper dar, die dunklen Rechtecke die beiden
Räder und der weiße Pfeil die Fahrtrichtung.
Zusätzlich zeigt eine 3D-Ansicht denselben Roboter und Rundkurs; ihre Perspektive
lässt sich mit der Maus drehen und zoomen. Der blaue Bewegungsverlauf wird in
der 2D-Ansicht angezeigt.
Der Rundkurs kann beliebig lange gefahren und pausiert werden. Mit den Reglern
lassen sich Breite, Höhe und Kurvenstärke einstellen; **Kurs übernehmen /
Zurücksetzen** übernimmt die Werte und setzt Roboter und Bewegungsverlauf zurück.
Danach kann die Simulation erneut gestartet werden. Mit **Manuell** lässt sich
der Roboter mit W (vorwärts),
S (rückwärts), A (links) und D (rechts) steuern. Die zuletzt gedrückte Taste
bestimmt die Bewegung; beim Loslassen hält der Roboter an. Der Browser muss
den Fokus haben. Mit **Linienfolger** übernimmt der Regler wieder.
Der sichtbare Bereich ist begrenzt; der Roboter kann ihn manuell verlassen.
Die Anzeige „Abstand zur Linie“ zeigt den kürzesten Abstand zum dargestellten
Kurs. Für einen Vergleich unter gleichen Startbedingungen vor jeder Fahrt
**Kurs übernehmen / Zurücksetzen** wählen.

Der Kurs ist durch `r(t) = 1 + Kurvenstärke * cos(3t)`,
`x(t) = Breite * r(t) * cos(t)` und `y(t) = Höhe * r(t) * sin(t)`
für `0 ≤ t ≤ 2π` beschrieben. Breite und Höhe sind Skalierungsfaktoren,
keine Gesamtabmessungen. Zeichnung, Abstandsmessung und Regler verwenden
dieselbe Näherung aus 360 verbundenen Punkten. Der Bewegungsverlauf zeigt die
letzten 2000 Zustände.

## Tests ausführen

Die Tests verwenden die eingebaute `unittest`-Bibliothek von Python:

```text
python -m unittest discover -s tests
```

Die NiceGUI-Oberfläche und die Konsolenausgabe nutzen denselben Simulationskern.
Ein Regler implementiert `ControllerPort`: Er liest den Roboterzustand und liefert
Radgeschwindigkeiten zurück. Die Simulation kann mit `set_controller(...)`
einen Regler verwenden; eine manuelle Tastatureingabe übernimmt wieder die
Steuerung. Der Rundkursregler verwendet den Roboterzustand und einen Zielpunkt
vor dem nächsten Kurspunkt. Simulierte Liniensensoren sind noch nicht enthalten.
