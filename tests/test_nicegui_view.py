import unittest
from math import pi
from unittest.mock import patch
from xml.etree import ElementTree

from src.adapters.nicegui_view import NiceGuiViewAdapter
from src.domain.robot import RobotState
from src.domain.track import RoundTrack


class NiceGuiViewTests(unittest.TestCase):
    @patch("src.adapters.nicegui_view.ui")
    def test_robot_body_and_wheels_rotate_with_heading(self, ui) -> None:
        view = NiceGuiViewAdapter(RoundTrack())
        view.show_robot(RobotState(x=1.0, y=0.5, heading=pi / 2))

        svg = ui.html.return_value.set_content.call_args.args[0]
        root = ElementTree.fromstring(svg)
        robot = root.find("g")
        self.assertIsNotNone(robot)
        self.assertEqual(robot.get("transform"), "translate(380.00 110.00) rotate(-90.00)")
        self.assertEqual(len(robot.findall("circle")), 1)
        wheels = robot.findall("rect")
        self.assertEqual(len(wheels), 2)
        self.assertEqual([wheel.get("y") for wheel in wheels], ["-24", "16"])
        self.assertEqual(len(robot.findall("path")), 1)

    @patch("src.adapters.nicegui_view.ui")
    def test_distance_is_measured_to_round_track(self, ui) -> None:
        track = RoundTrack()
        view = NiceGuiViewAdapter(track)
        distance_label = ui.label.return_value
        start = track.point(0)

        view.show_robot(RobotState(x=start.x, y=start.y, heading=0.0))
        distance_label.set_text.assert_called_with("Abstand zur Linie: 0.00")


if __name__ == "__main__":
    unittest.main()
