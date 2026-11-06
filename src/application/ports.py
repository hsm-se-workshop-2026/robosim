from typing import Protocol

from src.domain.robot import RobotState, WheelSpeeds


class SimulationInputPort(Protocol):
    def set_wheel_speeds(self, left_speed: float, right_speed: float) -> None:
        """Setzt die Sollgeschwindigkeit der beiden Räder."""

    def step(self, time_step: float) -> RobotState:
        """Führt einen Simulationsschritt aus und liefert den neuen Zustand."""


class RobotViewPort(Protocol):
    def show_robot(self, state: RobotState) -> None:
        """Zeigt einen Roboterzustand an."""


class ControllerPort(Protocol):
    def calculate(self, state: RobotState) -> WheelSpeeds:
        """Berechnet Radgeschwindigkeiten aus dem aktuellen Roboterzustand."""
