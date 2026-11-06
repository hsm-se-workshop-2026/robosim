from src.application.ports import ControllerPort, RobotViewPort, SimulationInputPort
from src.domain.robot import DifferentialDriveRobot, RobotState, WheelSpeeds


class SimulationService(SimulationInputPort):
    def __init__(self, robot: DifferentialDriveRobot, view: RobotViewPort) -> None:
        self._robot = robot
        self._view = view
        self._left_speed = 0.0
        self._right_speed = 0.0
        self._controller: ControllerPort | None = None

    def set_wheel_speeds(self, left_speed: float, right_speed: float) -> None:
        self._controller = None
        self._left_speed = left_speed
        self._right_speed = right_speed

    def set_controller(self, controller: ControllerPort | None) -> None:
        self._controller = controller

    def step(self, time_step: float) -> RobotState:
        if self._controller is not None:
            speeds: WheelSpeeds = self._controller.calculate(self._robot.state)
            self._left_speed = speeds.left
            self._right_speed = speeds.right

        state = self._robot.move(
            self._left_speed,
            self._right_speed,
            time_step,
        )
        self._view.show_robot(state)
        return state
