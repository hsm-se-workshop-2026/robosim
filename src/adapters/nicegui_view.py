from math import degrees

from nicegui import ui

from src.domain.robot import RobotState
from src.domain.track import Point, RoundTrack


class NiceGuiViewAdapter:
    def __init__(self, track: RoundTrack) -> None:
        self._track = track
        self._points: list[str] = []
        self._drawing = ui.html(sanitize=False)
        self._status = ui.label()
        self._distance = ui.label()

    def reset(self, track: RoundTrack) -> None:
        self._track = track
        self._points.clear()

    def show_robot(self, state: RobotState) -> None:
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
