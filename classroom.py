"""
Definiert den Grundriss eines Klassenzimmers als 2D-Zeichenarray.
Sitzplätze werden durch Richtungsbuchstaben (N/S/E/W) markiert;
andere Zeichen stehen für Tafel, Fenster oder leere Fläche.
"""
from dataclasses import dataclass


@dataclass
class Classroom:
    """Repräsentiert ein Klassenzimmer als Grundriss mit Sitzplätzen.

    Grundriss-Zellen:
    - '-' leere Bodenfläche
    - 'b' (Tafel), '*' (Fenster)
    - 'N', 'S', 'E', 'W': besetztbare Sitzplätze mit Blickrichtung
    """

    layout: list[list[str]]  # Grundriss als 2D-Zeichenarray

    @property
    def height(self) -> int:
        """Höhe des Grundrisses (Anzahl Reihen)."""
        return len(self.layout)

    @property
    def width(self) -> int:
        """Breite des Grundrisses (Anzahl Spalten)."""
        return len(self.layout[0]) if self.layout else 0

    def is_seat(self, row: int, col: int) -> bool:
        """Prüft, ob eine Position ein Sitzplatz (N, S, E, W) ist."""
        if row < 0 or col < 0 or row >= self.height or col >= self.width:
            return False
        return self.layout[row][col] in ("N", "S", "E", "W")

    def get_seats(self) -> list[tuple[int, int]]:
        """Alle möglichen Sitzplätze als Liste."""
        seats = []
        for row in range(self.height):
            for col in range(self.width):
                if self.is_seat(row, col):
                    seats.append((row, col))
        return seats


# Vorgefertigte Klassenzimmer-Instanz
default_classroom = Classroom(
    layout=[
        ["-", "-", "-", "b", "b", "b", "b", "-", "-", "-", "-", "-"],
        ["*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["*", "-", "N", "N", "N", "N", "N", "N", "N", "N", "-", "-"],
        ["*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["*", "-", "N", "N", "N", "N", "N", "N", "N", "N", "-", "-"],
        ["*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["*", "-", "N", "N", "N", "N", "N", "N", "N", "N", "-", "-"],
        ["*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["*", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["*", "-", "N", "N", "N", "N", "N", "N", "N", "N", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
        ["-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"],
    ],
)
