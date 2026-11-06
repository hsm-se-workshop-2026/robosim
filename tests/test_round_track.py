import unittest
from itertools import product
from math import hypot, pi

from src.adapters.line_follower import RoundTrackFollowerController
from src.domain.robot import DifferentialDriveRobot, RobotState
from src.domain.track import Point, RoundTrack


class RoundTrackTests(unittest.TestCase):
    def test_track_is_closed_and_parameters_change_its_shape(self) -> None:
        track = RoundTrack()
        start = track.point(0)
        end = track.point(2 * pi)
        self.assertAlmostEqual(start.x, end.x)
        self.assertAlmostEqual(start.y, end.y)
        self.assertNotEqual(track.point(0), RoundTrack(width=2.2).point(0))
        self.assertNotEqual(track.point(pi / 2), RoundTrack(height=0.8).point(pi / 2))
        self.assertNotEqual(track.point(0), RoundTrack(curves=0.2).point(0))

    def test_nearest_distance_uses_track_not_y_coordinate(self) -> None:
        track = RoundTrack()
        start = track.point(0)
        _, _, distance = track.nearest(start)
        self.assertAlmostEqual(distance, 0.0)
        _, _, distance = track.nearest(Point(start.x + 0.3, start.y))
        self.assertAlmostEqual(distance, 0.3, places=2)

    def test_rejects_out_of_range_parameters(self) -> None:
        for kwargs in ({"width": 1.4}, {"height": 1.4}, {"curves": 0.0}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                RoundTrack(**kwargs)

    def test_controller_completes_lap_for_parameter_extremes(self) -> None:
        for width, height, curves in product((1.5, 2.2), (0.8, 1.3), (0.05, 0.2)):
            with self.subTest(width=width, height=height, curves=curves):
                track = RoundTrack(width, height, curves)
                start = track.point(0)
                robot = DifferentialDriveRobot(
                    initial_state=RobotState(start.x, start.y, pi / 2)
                )
                controller = RoundTrackFollowerController(track)
                previous_segment = 0
                progress = 0
                max_distance = 0.0
                for _ in range(650):
                    speeds = controller.calculate(robot.state)
                    state = robot.move(speeds.left, speeds.right, 0.05)
                    _, segment, distance = track.nearest(Point(state.x, state.y))
                    progress += (segment - previous_segment + 180) % 360 - 180
                    previous_segment = segment
                    max_distance = max(max_distance, distance)

                self.assertGreater(progress, 360)
                self.assertLess(max_distance, 0.1)
                self.assertLess(hypot(state.x, state.y), 3.0)


if __name__ == "__main__":
    unittest.main()
