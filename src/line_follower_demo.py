from src.adapters.console_view import ConsoleViewAdapter
from src.adapters.line_follower import StraightLineFollowerController
from src.application.simulation import SimulationService
from src.domain.robot import DifferentialDriveRobot, RobotState


def main() -> None:
    robot = DifferentialDriveRobot(
        initial_state=RobotState(x=0.0, y=1.0, heading=0.0)
    )
    view = ConsoleViewAdapter()
    simulation = SimulationService(robot, view)
    simulation.set_controller(StraightLineFollowerController(line_y=0.0))

    print("Linienfolger-Demo: Zielgerade liegt bei y = 0.")
    for _ in range(200):
        simulation.step(time_step=0.05)


if __name__ == "__main__":
    main()
