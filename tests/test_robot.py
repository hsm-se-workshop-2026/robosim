import unittest

from src.adapters.keyboard_control import KeyboardControlAdapter
from src.adapters.line_follower import StraightLineFollowerController
from src.application.simulation import SimulationService
from src.domain.robot import DifferentialDriveRobot, RobotState, WheelSpeeds


class RecordingView:
    def __init__(self) -> None:
        self.states: list[RobotState] = []

    def show_robot(self, state: RobotState) -> None:
        self.states.append(state)


class DifferentialDriveRobotTests(unittest.TestCase):
    def test_equal_wheel_speeds_move_straight_forward(self) -> None:
        robot = DifferentialDriveRobot()

        state = robot.move(left_speed=1.0, right_speed=1.0, time_step=0.5)

        self.assertAlmostEqual(state.x, 0.5)
        self.assertAlmostEqual(state.y, 0.0)
        self.assertAlmostEqual(state.heading, 0.0)

    def test_different_wheel_speeds_rotate_robot(self) -> None:
        robot = DifferentialDriveRobot(wheel_base=0.5)

        state = robot.move(left_speed=-1.0, right_speed=1.0, time_step=0.25)

        self.assertAlmostEqual(state.x, 0.0)
        self.assertAlmostEqual(state.y, 0.0)
        self.assertAlmostEqual(state.heading, 1.0)


class KeyboardControlTests(unittest.TestCase):
    def test_releasing_key_stops_robot(self) -> None:
        robot = DifferentialDriveRobot()
        view = RecordingView()
        simulation = SimulationService(robot, view)
        keyboard = KeyboardControlAdapter(simulation)

        keyboard.press("w")
        keyboard.update(0.5)
        moving_state = robot.state
        keyboard.release()
        keyboard.update(0.5)
        stopped_state = robot.state

        self.assertAlmostEqual(moving_state.x, 0.5)
        self.assertEqual(stopped_state, moving_state)
        self.assertEqual(view.states, [moving_state, stopped_state])


class ConstantController:
    def calculate(self, state: RobotState) -> WheelSpeeds:
        return WheelSpeeds(left=1.0, right=1.0)


class ControllerTests(unittest.TestCase):
    def test_controller_output_moves_robot(self) -> None:
        robot = DifferentialDriveRobot()
        view = RecordingView()
        simulation = SimulationService(robot, view)
        simulation.set_controller(ConstantController())

        state = simulation.step(0.5)

        self.assertAlmostEqual(state.x, 0.5)
        self.assertAlmostEqual(state.y, 0.0)
        self.assertAlmostEqual(state.heading, 0.0)

    def test_manual_input_overrides_controller_and_controller_can_resume(self) -> None:
        robot = DifferentialDriveRobot()
        simulation = SimulationService(robot, RecordingView())
        keyboard = KeyboardControlAdapter(simulation)
        controller = ConstantController()
        simulation.set_controller(controller)

        keyboard.press("s")
        reverse_state = simulation.step(0.5)
        self.assertAlmostEqual(reverse_state.x, -0.5)

        keyboard.release()
        self.assertEqual(simulation.step(0.5), reverse_state)

        simulation.set_controller(controller)
        resumed_state = simulation.step(0.5)
        self.assertAlmostEqual(resumed_state.x, 0.0)


class LineFollowerTests(unittest.TestCase):
    def test_controller_turns_towards_line(self) -> None:
        controller = StraightLineFollowerController(line_y=0.0)
        state = RobotState(x=0.0, y=1.0, heading=0.0)

        speeds = controller.calculate(state)

        self.assertGreater(speeds.left, speeds.right)

    def test_simulation_moves_towards_straight_line(self) -> None:
        robot = DifferentialDriveRobot(
            initial_state=RobotState(x=0.0, y=1.0, heading=0.0)
        )
        view = RecordingView()
        simulation = SimulationService(robot, view)
        simulation.set_controller(StraightLineFollowerController(line_y=0.0))

        for _ in range(200):
            state = simulation.step(0.05)

        self.assertLess(abs(state.y), 0.5)


if __name__ == "__main__":
    unittest.main()
