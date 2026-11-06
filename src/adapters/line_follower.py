from math import atan2, cos, sin

from src.application.ports import ControllerPort
from src.domain.robot import RobotState, WheelSpeeds
from src.domain.track import Point, RoundTrack


class RoundTrackFollowerController(ControllerPort):
    def __init__(self, track: RoundTrack, wheel_base: float = 0.5) -> None:
        if wheel_base <= 0:
            raise ValueError("Der Abstand zwischen den Rädern muss positiv sein.")
        self._track = track
        self._wheel_base = wheel_base

    def calculate(self, state: RobotState) -> WheelSpeeds:
        nearest, segment, _ = self._track.nearest(Point(state.x, state.y))
        target = self._track.ahead(nearest, segment, 0.4)
        direction = atan2(target.y - state.y, target.x - state.x)
        error = atan2(sin(direction - state.heading), cos(direction - state.heading))
        angular_speed = max(-2.5, min(2.5, 3.0 * error))
        turn_speed = angular_speed * self._wheel_base / 2
        return WheelSpeeds(left=0.5 - turn_speed, right=0.5 + turn_speed)


class StraightLineFollowerController(ControllerPort):
    def __init__(
        self,
        line_y: float = 0.0,
        forward_speed: float = 0.5,
        lateral_gain: float = 1.5,
        heading_gain: float = 2.0,
        wheel_base: float = 0.5,
    ) -> None:
        if forward_speed <= 0:
            raise ValueError("Die Vorwärtsgeschwindigkeit muss positiv sein.")
        if lateral_gain < 0 or heading_gain < 0:
            raise ValueError("Die Reglerverstärkungen dürfen nicht negativ sein.")
        if wheel_base <= 0:
            raise ValueError("Der Abstand zwischen den Rädern muss positiv sein.")

        self._line_y = line_y
        self._forward_speed = forward_speed
        self._lateral_gain = lateral_gain
        self._heading_gain = heading_gain
        self._wheel_base = wheel_base

    def calculate(self, state: RobotState) -> WheelSpeeds:
        lateral_error = self._line_y - state.y
        heading_error = atan2(-sin(state.heading), cos(state.heading))
        angular_speed = (
            self._lateral_gain * lateral_error
            + self._heading_gain * heading_error
        )
        turn_speed = angular_speed * self._wheel_base / 2

        return WheelSpeeds(
            left=self._forward_speed - turn_speed,
            right=self._forward_speed + turn_speed,
        )
