"""
Einstiegspunkt der Anwendung.
Definiert Model und Controller,
und startet die tkinter-GUI.
"""

from dataclasses import dataclass, field

from classroom import Classroom, default_classroom
from constraints import (
    active_constraints,
    generate_seating_plan,
    validate_seating_plan,
)
from gui import SeatingPlanGUI
from students import Student, student_list


# === MODEL ===
@dataclass
class Model:
    """Daten und Business-Logik der Anwendung."""

    classroom: Classroom
    students: list[Student]
    constraints: list
    assignments: dict = field(default_factory=dict)

    def assign_seats(self):
        """Generiert einen neuen Sitzplan."""
        self.assignments = generate_seating_plan(
            self.classroom, self.students.copy(), self.constraints
        )

    def is_valid(self) -> bool:
        """Prüft, ob der aktuelle Sitzplan gültig ist."""
        if not self.assignments:
            return True  # Unplatziert = gültig
        return validate_seating_plan(
            self.assignments, self.classroom, self.students, self.constraints
        )

    def get_failed_constraints(self) -> list[str]:
        """Gibt die Fehlerbeschreibungen der fehlgeschlagenen Constraints zurück."""
        if not self.assignments:
            return []
        return [
            c.error_message
            for c in self.constraints
            if not c.validate(self.assignments, self.classroom, self.students)
        ]


# === CONTROLLER ===
class Controller:
    """Reagiert auf Nutzereingaben und delegiert an das Model."""

    def __init__(self, model: Model):
        self.model = model

    def on_generate_requested(self):
        """Wird aufgerufen, wenn der Nutzer einen neuen Sitzplan anfordert."""
        self.model.assign_seats()


def main():
    """Einstiegspunkt: Initialisiert Model, Controller und GUI."""
    model = Model(
        classroom=default_classroom,
        students=student_list.copy(),
        constraints=active_constraints,
    )
    controller = Controller(model)

    app = SeatingPlanGUI(model=model, controller=controller)
    app.run()


if __name__ == "__main__":
    main()
