"""
Definiert Regeln (Constraints), die ein gültiger Sitzplan erfüllen muss.
Enthält Constraint-Klassen zur Validierung einzelner Regeln sowie
Hilfsfunktionen zum Generieren und Gesamtprüfen eines Sitzplans.
"""

import random
from abc import ABC, abstractmethod

from classroom import Classroom
from students import Student

# === CONSTRAINT-KLASSEN (Validierung) ===
# Jede Klasse prüft eine einzelne Regel und gibt True/False zurück.


class Constraint(ABC):
    """Abstrakte Basis-Klasse für alle Constraints."""

    error_message: str
    "Diese Meldung kann im Fehlerfall angezeigt werden"

    @abstractmethod
    def validate(
        self,
        assignments: dict[str, tuple],
        classroom: Classroom,
        students: list[Student],
    ) -> bool:
        """
        Validiert, ob die Zuweisung diese Regel erfüllt.

        Args:
            assignments: Zuordnung von Schülername zu Sitzplatz (Reihe, Spalte)
            classroom: Das Klassenzimmer mit seinem Grundriss
            students: Liste aller Schülerinnen und Schüler

        Returns: True wenn gültig, False sonst.
        """
        pass


class ConstraintX(Constraint):
    error_message = ""

    def validate(
        self,
        assignments: dict[str, tuple[int, int]],
        classroom: Classroom,
        students: list[Student],
    ) -> bool:
        occupied_positions = set(assignments.values())

        for student_name, (row, col) in assignments.items():
            neighbors = [
                (row - 1, col),
                (row + 1, col),
                (row, col - 1),
                (row, col + 1),
            ]

            has_neighbor = any(neighbor in occupied_positions for neighbor in neighbors)

            if not has_neighbor:
                return False

        return True


class NoDoubleAssignments(Constraint):
    """Keine Doppelbelegung auf einem Sitzplatz."""

    error_message = "Mehrere Schüler auf demselben Sitzplatz"

    def validate(
        self,
        assignments: dict[str, tuple],
        classroom: Classroom,
        students: list[Student],
    ) -> bool:
        # Prüfe auf doppelte Positionen
        positions_seen = set()
        for student_name, position in assignments.items():
            if position in positions_seen:
                return False
            positions_seen.add(position)

        return True


class SeatsExist(Constraint):
    """Alle zugewiesenen Sitzplätze existieren im Klassenzimmer"""

    error_message = "Sitzplätze existieren nicht im Klassenzimmer"

    def validate(
        self,
        assignments: dict[str, tuple],
        classroom: Classroom,
        students: list[Student],
    ) -> bool:
        for _, position in assignments.items():
            row, col = position
            if not classroom.is_seat(row, col):
                return False
        return True


# === AKTIVE REGELN ===
# Füge hier neue Regeln hinzu oder entferne sie:

active_constraints: list["Constraint"] = [
    NoDoubleAssignments(),
    SeatsExist(),
    # ConstraintX(),
]


# === GESAMTVALIDIERUNG ===


def validate_seating_plan(
    assignments: dict[str, tuple],
    classroom: Classroom,
    students: list[Student],
    constraints: list[Constraint],
) -> bool:
    """Prüft, ob ein Sitzplan alle Constraints erfüllt."""
    return all(c.validate(assignments, classroom, students) for c in constraints)


# === GENERIERUNG ===


def generate_seating_plan(
    classroom: Classroom, students: list[Student], constraints: list[Constraint]
) -> dict[str, tuple]:
    """Generiert einen Sitzplan."""
    assignments = {}
    random.shuffle(students)
    available_seats = classroom.get_seats()
    random.shuffle(available_seats)
    for student, position in zip(students, available_seats):
        assignments[student.name] = position

    return assignments
