from dataclasses import dataclass
from math import cos, hypot, pi, sin


@dataclass(frozen=True)
class Point:
    x: float
    y: float


class RoundTrack:
    """Geschlossener, parametrischer Rundkurs, gegen den Uhrzeigersinn."""

    def __init__(
        self, width: float = 1.9, height: float = 1.1, curves: float = 0.12
    ) -> None:
        if not 1.5 <= width <= 2.2:
            raise ValueError("Die Breite muss zwischen 1,5 und 2,2 liegen.")
        if not 0.8 <= height <= 1.3:
            raise ValueError("Die Höhe muss zwischen 0,8 und 1,3 liegen.")
        if not 0.05 <= curves <= 0.2:
            raise ValueError("Die Kurvenstärke muss zwischen 0,05 und 0,2 liegen.")
        self.width = width
        self.height = height
        self.curves = curves
        self.points = tuple(self.point(2 * pi * i / 360) for i in range(360))

    def point(self, parameter: float) -> Point:
        radius = 1 + self.curves * cos(3 * parameter)
        return Point(
            self.width * radius * cos(parameter),
            self.height * radius * sin(parameter),
        )

    def nearest(self, position: Point) -> tuple[Point, int, float]:
        best_distance_squared = float("inf")
        best_point = self.points[0]
        best_index = 0
        for index, start in enumerate(self.points):
            end = self.points[(index + 1) % len(self.points)]
            dx, dy = end.x - start.x, end.y - start.y
            fraction = ((position.x - start.x) * dx + (position.y - start.y) * dy) / (
                dx * dx + dy * dy
            )
            fraction = max(0.0, min(1.0, fraction))
            point = Point(start.x + fraction * dx, start.y + fraction * dy)
            distance_squared = (point.x - position.x) ** 2 + (point.y - position.y) ** 2
            if distance_squared < best_distance_squared:
                best_distance_squared = distance_squared
                best_point = point
                best_index = index
        return best_point, best_index, best_distance_squared ** 0.5

    def ahead(self, start: Point, segment: int, distance: float) -> Point:
        if distance < 0:
            raise ValueError("Der Vorausschauabstand darf nicht negativ sein.")
        current = start
        index = (segment + 1) % len(self.points)
        while True:
            target = self.points[index]
            length = hypot(target.x - current.x, target.y - current.y)
            if length > 0 and distance <= length:
                fraction = distance / length
                return Point(
                    current.x + fraction * (target.x - current.x),
                    current.y + fraction * (target.y - current.y),
                )
            distance -= length
            current = target
            index = (index + 1) % len(self.points)
