# User Stories

## MoSCoW-Priorisierung

- **Must Have**: erforderlich für eine nutzbare erste Version und die zentralen Lernziele.
- **Should Have**: wichtig, kann aber nach den Must-Have-Funktionen umgesetzt werden.
- **Could Have**: optional; erhöht den Nutzen, ist aber nicht erforderlich.
- **Won't Have (dieser Version)**: wird bewusst nicht in den Umfang dieser Version aufgenommen.

## Entwicklungsprozess und Grundlagen

### User Story 1

**Priorität: Should Have**

**Als Dozent** möchte ich die Schritte vom Steuereingang bis zur Roboterbewegung sichtbar machen, damit ich den Simulations- und Regelungsablauf im Unterricht erklären kann.

**Akzeptanzkriterien**
- Die Anwendung zeigt den aktuellen Steuereingang und die daraus resultierende Bewegung des Roboters.
- Studierende können den Zusammenhang zwischen Eingabe und Bewegung während der Simulation nachvollziehen.

### User Story 2

**Priorität: Must Have**

**Als Studierender** möchte ich die Bewegung eines differentiell angetriebenen Roboters beobachten, damit ich den Zusammenhang zwischen Steuerung und Bewegung nachvollziehen kann.

**Akzeptanzkriterien**
- Die Simulation zeigt einen differentiell angetriebenen Roboter in einer Umgebung.
- Änderungen an den Steuereingängen wirken sich in der Simulation auf die Bewegung aus.

## Steuerung und Regelung

### User Story 3

**Priorität: Must Have**

**Als Studierender** möchte ich den Roboter per Tastatur steuern, damit ich sein Verhalten mit dem eines Reglers vergleichen kann.

**Akzeptanzkriterien**
- Tastatureingaben steuern die Bewegung des Roboters während der Simulation.
- Werden die Steuerungstasten losgelassen, endet die manuelle Bewegung.

### User Story 4

**Priorität: Should Have**

**Als Studierender** möchte ich einen Regler für eine Simulation auswählen und ausführen, damit ich verschiedene Regelungsansätze erproben kann.

**Akzeptanzkriterien**
- Ein Regler kann für eine Simulation ausgewählt und gestartet werden.
- Der ausgewählte Regler steuert den Roboter ohne fortlaufende manuelle Eingaben.

## Visualisierung und Linienfolger

### User Story 5

**Priorität: Must Have**

**Als Studierender** möchte ich den Roboter, die Fahrspur und seinen Bewegungsverlauf sehen, damit ich erkennen kann, wie gut der Roboter der Spur folgt.

**Akzeptanzkriterien**
- Die Visualisierung zeigt Roboter und Fahrspur während der Simulation.
- Der Bewegungsverlauf des Roboters ist in der Visualisierung erkennbar.

### User Story 6

**Priorität: Must Have**

**Als Dozent** möchte ich eine Linienfolger-Demo starten können, damit ich die Anwendung eines Reglers an einem konkreten Beispiel zeigen kann.

**Akzeptanzkriterien**
- Die Demo startet mit einem Roboter, einer Linie und einem zugeordneten Regler.
- Während der Demo ist sichtbar, wie der Roboter der Linie folgt.
