"""Small JSON interface between the simulation and the static browser UI."""

import json
from math import pi

from src.adapters.keyboard_control import KeyboardControlAdapter
from src.adapters.line_follower import RoundTrackFollowerController
from src.application.simulation import SimulationService
from src.domain.robot import DifferentialDriveRobot, RobotState
from src.domain.track import Point, RoundTrack


class _NullView:
    def show_robot(self, state: RobotState) -> None:
        pass


_track: RoundTrack
_robot: DifferentialDriveRobot
_simulation: SimulationService
_controller: RoundTrackFollowerController
_keyboard: KeyboardControlAdapter
_manual = False


def reset(width: float = 1.9, height: float = 1.1, curves: float = 0.12) -> str:
    global _track, _robot, _simulation, _controller, _keyboard, _manual

    _track = RoundTrack(float(width), float(height), float(curves))
    start = _track.point(0)
    _robot = DifferentialDriveRobot(
        initial_state=RobotState(start.x, start.y, pi / 2)
    )
    _simulation = SimulationService(_robot, _NullView())
    _controller = RoundTrackFollowerController(_track, _robot.wheel_base)
    _simulation.set_controller(_controller)
    _keyboard = KeyboardControlAdapter(_simulation)
    _manual = False
    return snapshot(include_track=True)


def set_mode(mode: str) -> None:
    global _manual

    if mode not in ("manual", "controller"):
        raise ValueError("Unbekannter Steuerungsmodus.")
    if mode == "manual":
        _simulation.set_controller(None)
        _keyboard.release()
        _manual = True
    else:
        _keyboard.release()
        _simulation.set_controller(_controller)
        _manual = False


def press_key(key: str) -> None:
    if not _manual:
        raise RuntimeError("Manuelle Eingaben sind nur im manuellen Modus erlaubt.")
    if key.lower() not in ("w", "a", "s", "d"):
        raise ValueError("Erlaubte Tasten sind W, A, S und D.")
    _keyboard.press(key.lower())


def release_key() -> None:
    if _manual:
        _keyboard.release()


def step(time_step: float = 0.05) -> str:
    _simulation.step(float(time_step))
    return snapshot()


def snapshot(include_track: bool = False) -> str:
    state = _robot.state
    _, _, distance = _track.nearest(Point(state.x, state.y))
    result = {
        "x": state.x,
        "y": state.y,
        "heading": state.heading,
        "distance": distance,
    }
    if include_track:
        result["track"] = [
            {"x": point.x, "y": point.y} for point in _track.points
        ]
    return json.dumps(result)


reset()
