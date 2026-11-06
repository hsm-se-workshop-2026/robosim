---
marp: true
theme: default
paginate: true
size: 16:9
---

<!-- _class: lead -->

# RoboSim

## Einen Roboter simulieren und steuern

Ein Lernprojekt für Software Engineering und Regelungstechnik

---

# Die Projektidee

- Einen Roboter mit **zwei unabhängig angetriebenen Rädern** simulieren
- Seine Bewegung im Browser sichtbar machen
- Selbst steuern und mit einem automatischen Regler vergleichen
- Softwareentwicklung anhand eines greifbaren Beispiels kennenlernen

---

# Was kann RoboSim?

- **Manuell fahren:** mit W, A, S und D
- **Automatisch fahren:** ein Regler folgt einem Rundkurs
- **Kurs verändern:** Breite, Höhe und Kurvenstärke einstellen
- **Beobachten:** Roboter, Bewegungsverlauf und Abstand zur Linie

---

# Live-Demo

1. Im Projektordner starten:

   ```text
   python -m src.web_demo
   ```

2. `http://127.0.0.1:8093` im Browser öffnen.
3. **Start / Fortsetzen** wählen und den Linienfolger beobachten.
4. Zu **Manuell** wechseln und mit W/A/S/D fahren.
5. Kursparameter ändern und **Kurs übernehmen / Zurücksetzen** wählen.

---

# Wie bewegt sich der Roboter?

Der Roboter hat einen **Differentialantrieb**:

| Radgeschwindigkeiten | Bewegung |
|---|---|
| Beide Räder gleich schnell | Geradeaus |
| Räder unterschiedlich schnell | Kurvenfahrt |
| Räder entgegengesetzt | Drehung auf der Stelle |

Die Simulation berechnet Position und Ausrichtung in kleinen Zeitschritten.

```text
                 Fahrtrichtung
                      ^
          +-----------------------+
          |      ROBOTER          |
          |  [linkes]   [rechtes] |  <- Antriebsraeder
          +-----------------------+
                Radabstand
```

---

# Wie folgt der Regler dem Kurs?

1. Den nächstgelegenen Punkt auf dem Kurs suchen.
2. Einen Zielpunkt ein Stück **vor** diesem Punkt bestimmen.
3. Die Richtung zum Ziel mit der aktuellen Ausrichtung vergleichen.
4. Daraus Geschwindigkeiten für linkes und rechtes Rad berechnen.

```text
+----------------------+    +----------------------+    +----------------------+
| Roboterposition      | -> | Punkt am Kurs        | -> | Ziel voraus          |
+----------------------+    +----------------------+    +----------------------+
                                                           |
                                                           v
+----------------------+    +----------------------+    +----------------------+
| Raeder ansteuern     | <- | Richtung abgleichen  | <- | Ist-Ausrichtung      |
+----------------------+    +----------------------+    +----------------------+
       ^                                                   |
       +---------------- naechster Zeitschritt <-----------+
```

Der Rundkursregler verwendet die simulierte Position und den bekannten Kurs;
**Liniensensoren werden bisher nicht simuliert**.

---

# Der Rundkurs

- Geschlossene, parametrische Kurve mit mehreren Wölbungen
- **Breite** und **Höhe** skalieren die Form
- **Kurvenstärke** verändert die Wölbungen
- Eine Linie aus 360 verbundenen Punkten nähert den Kurs an

Dieselbe Kursnäherung dient der Darstellung, Abstandsmessung und Regelung.

```text
                    .---->----.
                 .-'           '-.
               .'                 '.
              /                     \
             |                       |
              \                     /
               '.                 .'
                 '-.___________.-'

             geschlossener Rundkurs
```

---

# Architektur: getrennte Aufgaben

Die Anwendung orientiert sich an einer **hexagonalen Architektur**:

```text
Tastatur → Adapter → Simulation → Robotermodell
                         ├──────→ Regler → Rundkurs
                         └──────→ Anzeige → Browser
```

**Ports** beschreiben Schnittstellen; **Adapter** verbinden die Simulation
mit Tastatur, Regler und Anzeige. Der Simulationskern benötigt kein NiceGUI.

---

# Qualität und nächste Schritte

- Automatische Tests prüfen Bewegung, Regler, Rundkurs und Darstellung.
- Der aktuelle Regler kennt Position und Kurs direkt.
- **Mögliche Erweiterungen:** Liniensensoren simulieren, weitere Regler
  vergleichen und Vergleichskennzahlen ergänzen.

Weitere Details: [Code-Dokumentation](./code-dokumentation.md) ·
[Architekturdiagramm](./architektur.puml)

---

<!-- _class: lead -->

# Fragen?

**RoboSim:** Softwarearchitektur und Regelung interaktiv erleben.
