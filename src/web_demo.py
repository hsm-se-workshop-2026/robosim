from math import pi

from nicegui import events, ui

from src.adapters.keyboard_control import KeyboardControlAdapter
from src.adapters.line_follower import RoundTrackFollowerController
from src.adapters.nicegui_view import NiceGuiViewAdapter
from src.application.simulation import SimulationService
from src.domain.robot import DifferentialDriveRobot, RobotState
from src.domain.track import RoundTrack


@ui.page("/")
def page() -> None:
    ui.label("Roboter-Demo").classes("text-h5")
    ui.label("Schwarz: Linie · Rot: Roboter · Blau: Bewegungsverlauf · Weiß: Fahrtrichtung")
    ui.label("Manuell: W vorwärts, S rückwärts, A links, D rechts (eine Taste gleichzeitig)")

    track = RoundTrack()
    start_point = track.point(0)
    robot = DifferentialDriveRobot(
        initial_state=RobotState(x=start_point.x, y=start_point.y, heading=pi / 2)
    )
    view = NiceGuiViewAdapter(track)
    view.show_robot(robot.state)
    simulation = SimulationService(robot, view)
    controller = RoundTrackFollowerController(track, wheel_base=robot.wheel_base)
    simulation.set_controller(controller)
    keyboard = KeyboardControlAdapter(simulation)

    manual = False
    active_key: str | None = None
    status = ui.label("Bereit")
    mode_status = ui.label("Modus: Linienfolger")

    def stop_manual() -> None:
        nonlocal active_key
        active_key = None
        if manual:
            keyboard.release()

    def select_manual() -> None:
        nonlocal manual
        manual = True
        stop_manual()
        mode_status.set_text("Modus: Manuell")

    def select_controller() -> None:
        nonlocal manual
        stop_manual()
        manual = False
        simulation.set_controller(controller)
        mode_status.set_text("Modus: Linienfolger")

    def handle_key(event: events.KeyEventArguments) -> None:
        nonlocal active_key
        key = event.key.name.lower()
        if not manual or not timer.active or key not in ("w", "a", "s", "d"):
            return
        if event.action.keydown and not event.action.repeat:
            active_key = key
            keyboard.press(key)
        elif event.action.keyup and key == active_key:
            stop_manual()

    ui.keyboard(on_key=handle_key, ignore=[])
    ui.on("robosim_focus_lost", stop_manual)
    ui.run_javascript(
        "window.addEventListener('blur', () => emitEvent('robosim_focus_lost'))"
    )

    def advance() -> None:
        simulation.step(0.05)

    timer = ui.timer(0.05, advance, active=False)

    def start() -> None:
        timer.active = True
        status.set_text("Simulation läuft")

    def pause() -> None:
        timer.active = False
        stop_manual()
        status.set_text("Pausiert")

    ui.context.client.on_disconnect(pause)

    def apply_track() -> None:
        nonlocal track, robot, simulation, controller, keyboard, manual
        if width.value is None or height.value is None or curves.value is None:
            ui.notify("Bitte alle Kursparameter auswählen.", type="negative")
            return
        pause()
        track = RoundTrack(width.value, height.value, curves.value)
        start_point = track.point(0)
        robot = DifferentialDriveRobot(
            initial_state=RobotState(start_point.x, start_point.y, pi / 2)
        )
        view.reset(track)
        view.show_robot(robot.state)
        simulation = SimulationService(robot, view)
        controller = RoundTrackFollowerController(track, wheel_base=robot.wheel_base)
        simulation.set_controller(controller)
        keyboard = KeyboardControlAdapter(simulation)
        manual = False
        mode_status.set_text("Modus: Linienfolger")
        status.set_text("Kurs übernommen – bereit")

    ui.label("Kursparameter (übernehmen setzt die Simulation zurück)")
    ui.label("Breite")
    width = ui.slider(min=1.5, max=2.2, step=0.1, value=1.9).props("label-always")
    ui.label("Höhe")
    height = ui.slider(min=0.8, max=1.3, step=0.1, value=1.1).props("label-always")
    ui.label("Kurvenstärke")
    curves = ui.slider(min=0.05, max=0.2, step=0.01, value=0.12).props("label-always")
    ui.button("Kurs übernehmen / Zurücksetzen", on_click=apply_track)

    with ui.row():
        ui.button("Manuell", on_click=select_manual)
        ui.button("Linienfolger", on_click=select_controller)

    with ui.row():
        ui.button("Start / Fortsetzen", on_click=start)
        ui.button("Pause", on_click=pause)


def main() -> None:
    ui.run(title="RoboSim: Linienfolger", host="127.0.0.1", port=8093, reload=False)


if __name__ == "__main__":
    main()
