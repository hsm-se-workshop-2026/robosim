from math import degrees, pi

from nicegui import ui
from nicegui.elements.scene.objects.polyline import Polyline

from src.domain.robot import RobotState
from src.domain.track import Point, RoundTrack


class NiceGuiViewAdapter:
    def __init__(self, track: RoundTrack) -> None:
        self._track = track
        self._points: list[str] = []
        ui.label("2D-Ansicht mit Bewegungsverlauf")
        self._drawing = ui.html(sanitize=False)
        self._status = ui.label()
        self._distance = ui.label()
        ui.label("3D-Ansicht: mit der Maus drehen und zoomen")
        self._scene = ui.scene(width=600, height=350, grid=(10, 20)).classes("max-w-full")
        with self._scene:
            self._track_line = self._draw_track()
            self._robot_3d = self._scene.group()
            with self._robot_3d:
                self._scene.cylinder(0.25, 0.25, 0.16, 32).material(
                    "#e53935"
                ).rotate(pi / 2, 0, 0).move(z=0.16)
                for y in (-0.25, 0.25):
                    self._scene.box(0.22, 0.09, 0.16).material("#333333").move(
                        y=y, z=0.08
                    )
                self._scene.extrusion(
                    [[0.04, -0.07], [0.19, 0], [0.04, 0.07]], 0.01
                ).material("#ffffff").move(z=0.245)

    def _draw_track(self) -> Polyline:
        points = [[point.x, point.y, 0.01] for point in self._track.points]
        points.append(points[0])
        return self._scene.polyline(points).material("#333333")

    def reset(self, track: RoundTrack) -> None:
        self._track = track
        self._points.clear()
        self._track_line.delete()
        with self._scene:
            self._track_line = self._draw_track()

    def show_robot(self, state: RobotState) -> None:
        self._robot_3d.move(state.x, state.y, 0)
        self._robot_3d.rotate(0, 0, state.heading)
        x = 300 + state.x * 80
        y = 150 - state.y * 80
        self._points.append(f"{x:.2f},{y:.2f}")
        if len(self._points) > 2000:
            self._points.pop(0)
        points = " ".join(self._points)
        track_points = " ".join(
            f"{300 + point.x * 80:.2f},{150 - point.y * 80:.2f}"
            for point in self._track.points
        )
        self._drawing.set_content(
            '<svg viewBox="0 0 600 300" width="600" '
            'style="max-width: 100%; border: 1px solid #999" '
            'role="img" aria-label="Roboter und Linienverlauf">'
            f'<polygon points="{track_points}" fill="none" '
            'stroke="#333" stroke-width="3" />'
            f'<polyline points="{points}" fill="none" stroke="#1976d2" '
            'stroke-width="2" />'
            f'<g transform="translate({x:.2f} {y:.2f}) '
            f'rotate({-degrees(state.heading):.2f})">'
            '<circle cx="0" cy="0" r="20" fill="#e53935" '
            'stroke="#b71c1c" stroke-width="2" />'
            '<rect x="-9" y="-24" width="18" height="8" rx="2" fill="#333" />'
            '<rect x="-9" y="16" width="18" height="8" rx="2" fill="#333" />'
            '<path d="M 4 -5 L 14 0 L 4 5 Z" fill="white" />'
            '</g>'
            '</svg>'
        )
        self._status.set_text(
            f"x = {state.x:.2f}, y = {state.y:.2f}, "
            f"Winkel = {state.heading:.2f} rad"
        )
        _, _, distance = self._track.nearest(Point(state.x, state.y))
        self._distance.set_text(f"Abstand zur Linie: {distance:.2f}")
