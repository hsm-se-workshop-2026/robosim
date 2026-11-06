from src.adapters.console_view import ConsoleViewAdapter
from src.adapters.keyboard_control import KeyboardControlAdapter
from src.application.simulation import SimulationService
from src.domain.robot import DifferentialDriveRobot


def main() -> None:
    robot = DifferentialDriveRobot()
    view = ConsoleViewAdapter()
    simulation = SimulationService(robot, view)
    keyboard = KeyboardControlAdapter(simulation)

    print("Vorwärts fahren:")
    keyboard.press("w")
    for _ in range(5):
        keyboard.update(time_step=0.1)

    print("Anhalten:")
    keyboard.release()
    keyboard.update(time_step=0.1)


if __name__ == "__main__":
    main()
