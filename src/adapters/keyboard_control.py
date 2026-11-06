from src.application.ports import SimulationInputPort


class KeyboardControlAdapter:
    def __init__(self, simulation: SimulationInputPort, speed: float = 1.0) -> None:
        self._simulation = simulation
        self._speed = speed

    def press(self, key: str) -> None:
        commands = {
            "w": (self._speed, self._speed),
            "s": (-self._speed, -self._speed),
            "a": (-self._speed, self._speed),
            "d": (self._speed, -self._speed),
        }
        left_speed, right_speed = commands.get(key.lower(), (0.0, 0.0))
        self._simulation.set_wheel_speeds(left_speed, right_speed)

    def release(self) -> None:
        self._simulation.set_wheel_speeds(0.0, 0.0)

    def update(self, time_step: float) -> None:
        self._simulation.step(time_step)
