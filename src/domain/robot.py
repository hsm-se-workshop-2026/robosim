from dataclasses import dataclass
from math import cos, sin


@dataclass(frozen=True)
class RobotState:
    x: float
    y: float
    heading: float


@dataclass(frozen=True)
class WheelSpeeds:
    left: float
    right: float


class DifferentialDriveRobot:
    def __init__(
        self,
        wheel_base: float = 0.5,
        initial_state: RobotState | None = None,
    ) -> None:
        if wheel_base <= 0:
            raise ValueError("Der Abstand zwischen den Rädern muss positiv sein.")
        self.wheel_base = wheel_base
        if initial_state is None:
            initial_state = RobotState(x=0.0, y=0.0, heading=0.0)
        self._state = initial_state

    @property
    def state(self) -> RobotState:
        return self._state

    def move(self, left_speed: float, right_speed: float, time_step: float) -> RobotState:
        if time_step < 0:
            raise ValueError("Der Simulationszeitschritt darf nicht negativ sein.")

        linear_speed = (left_speed + right_speed) / 2
        angular_speed = (right_speed - left_speed) / self.wheel_base
        heading = self._state.heading

        self._state = RobotState(
            x=self._state.x + linear_speed * cos(heading) * time_step,
            y=self._state.y + linear_speed * sin(heading) * time_step,
            heading=heading + angular_speed * time_step,
        )
        return self._state
