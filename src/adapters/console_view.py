from src.domain.robot import RobotState


class ConsoleViewAdapter:
    def show_robot(self, state: RobotState) -> None:
        print(
            f"Roboter: x={state.x:.2f}, y={state.y:.2f}, "
            f"Winkel={state.heading:.2f} rad"
        )
