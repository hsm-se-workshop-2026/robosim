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

    @patch("src.adapters.nicegui_view.ui")
    def test_3d_robot_uses_simulation_position_and_heading(self, ui) -> None:
        view = NiceGuiViewAdapter(RoundTrack())
        scene = ui.scene.return_value.classes.return_value
        robot = scene.group.return_value

        view.show_robot(RobotState(x=1.0, y=-0.5, heading=pi / 2))

        robot.move.assert_called_with(1.0, -0.5, 0)
        robot.rotate.assert_called_with(0, 0, pi / 2)

    @patch("src.adapters.nicegui_view.ui")
    def test_3d_track_is_closed_and_replaced_on_reset(self, ui) -> None:
        track = RoundTrack()
        view = NiceGuiViewAdapter(track)
        scene = ui.scene.return_value.classes.return_value
        old_line = scene.polyline.return_value.material.return_value
        points = scene.polyline.call_args.args[0]
        self.assertEqual(len(points), 361)
        self.assertEqual(points[0], points[-1])
        self.assertEqual(points[0], [track.points[0].x, track.points[0].y, 0.01])

        new_track = RoundTrack(width=2.2, height=1.3, curves=0.2)
        view.show_robot(RobotState(0, 0, 0))
        view.reset(new_track)
        old_line.delete.assert_called_once()
        points = scene.polyline.call_args.args[0]
        self.assertEqual(scene.polyline.call_count, 2)
        self.assertEqual(points[0], [new_track.points[0].x, new_track.points[0].y, 0.01])
        self.assertEqual(points[0], points[-1])
        view.show_robot(RobotState(1, 0, 0))
        svg = ui.html.return_value.set_content.call_args.args[0]
        root = ElementTree.fromstring(svg)
        self.assertEqual(root.find("polyline").get("points"), "380.00,150.00")


if __name__ == "__main__":
    unittest.main()
