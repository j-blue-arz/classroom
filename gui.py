"""
Grafische Oberfläche des Sitzplan-Generators.
"""

import tkinter as tk
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import Controller, Model


# Konstanten für die Visualisierung
CELL_SIZE = 50
DESK_SIZE = 40
CHAIR_SIZE = 12


def classroom_to_canvas(row, col) -> tuple[int, int]:
    """Berechnet den Canvas-Ursprung (oben links) einer Zelle im Classroom."""
    return col * CELL_SIZE, row * CELL_SIZE


def canvas_to_classroom(x, y) -> tuple[int, int] | None:
    """Berechnen den Zell-Index, der einem Punkt auf dem Canvas entspricht."""
    pass


class ClassroomCanvas:
    """Kapselt das Canvas und zeichnet den Classroom-Inhalt."""

    def __init__(self, parent_frame, model: "Model"):
        self.model = model

        canvas_width = int(1200 * 0.85)
        canvas_height = 650
        self.canvas = tk.Canvas(
            parent_frame,
            width=canvas_width,
            height=canvas_height,
            bg="white",
            border=2,
            relief=tk.SUNKEN,
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, padx=20, pady=20, expand=True)

    def draw(self):
        """Zeichnet den Classroom neu."""
        self.canvas.delete("all")

        classroom = self.model.classroom

        # Wand zeichnen
        self._draw_wall(classroom)

        # Tafel und vordefinierte Sitzplätze (mit Blickrichtung im Grundriss)
        for row in range(classroom.height):
            for col in range(classroom.width):
                cell = classroom.layout[row][col]
                if cell == "b":
                    self._draw_board(row, col)
                elif cell in ("N", "S", "E", "W"):
                    # Sitzplatz mit vorgegebener Richtung
                    self._draw_desk((row, col))
                    self._draw_chair((row, col), cell)

        # Namen auf den Tischen (Zuweisungen)
        for student_name, position in self.model.assignments.items():
            self._draw_student_name(position, student_name)

    def _draw_wall(self, classroom):
        """Zeichnet die Klassenzimmer-Wand als Box um den Grundriss."""
        x0 = 0
        y0 = 0
        x1 = classroom.width * CELL_SIZE
        y1 = classroom.height * CELL_SIZE
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", width=2)

    def _draw_board(self, row, col):
        """Zeichnet ein Tafel-Feld (dunkelgrün, dick)."""
        x0, y0 = classroom_to_canvas(row, col)
        x1 = x0 + CELL_SIZE
        y1 = y0 + CELL_SIZE
        self.canvas.create_rectangle(
            x0, y0, x1, y1, fill="darkgreen", outline="darkgreen", width=3
        )

    def _draw_desk(self, position):
        """Zeichnet einen Schreibtisch."""
        row, col = position
        cell_x, cell_y = classroom_to_canvas(row, col)
        desk_x = cell_x + (CELL_SIZE - DESK_SIZE) // 2
        desk_y = cell_y + (CELL_SIZE - DESK_SIZE) // 2

        self.canvas.create_rectangle(
            desk_x,
            desk_y,
            desk_x + DESK_SIZE,
            desk_y + DESK_SIZE,
            fill="lightyellow",
            outline="orange",
            width=2,
        )

    def _draw_chair(self, position, direction_code):
        """Zeichnet einen Stuhl mit Blickrichtung."""
        row, col = position
        cell_x, cell_y = classroom_to_canvas(row, col)
        desk_x = cell_x + (CELL_SIZE - DESK_SIZE) // 2
        desk_y = cell_y + (CELL_SIZE - DESK_SIZE) // 2

        chair_x, chair_y = self._calculate_chair_position(
            desk_x, desk_y, direction_code
        )
        self.canvas.create_rectangle(
            chair_x - CHAIR_SIZE // 2,
            chair_y - CHAIR_SIZE // 2,
            chair_x + CHAIR_SIZE // 2,
            chair_y + CHAIR_SIZE // 2,
            fill="brown",
            outline="black",
            width=1,
        )

    def _draw_student_name(self, position, name):
        """Zeichnet den Namen eines Schülers auf dem Tisch."""
        row, col = position
        cell_x, cell_y = classroom_to_canvas(row, col)
        desk_x = cell_x + (CELL_SIZE - DESK_SIZE) // 2
        desk_y = cell_y + (CELL_SIZE - DESK_SIZE) // 2

        self.canvas.create_text(
            desk_x + DESK_SIZE // 2,
            desk_y + DESK_SIZE // 2,
            text=name,
            fill="darkblue",
            font=("Arial", 8, "bold"),
        )

    def _calculate_chair_position(self, desk_x, desk_y, direction_code):
        """Berechnet die Stuhlposition basierend auf Blickrichtung."""
        desk_center_x = desk_x + DESK_SIZE // 2
        desk_center_y = desk_y + DESK_SIZE // 2

        if direction_code == "N":  # NORTH
            return desk_center_x, desk_y + DESK_SIZE + 5
        elif direction_code == "S":  # SOUTH
            return desk_center_x, desk_y - 5
        elif direction_code == "E":  # EAST
            return desk_x - 5, desk_center_y
        elif direction_code == "W":  # WEST
            return desk_x + DESK_SIZE + 5, desk_center_y

        return desk_center_x, desk_center_y


class SeatingPlanGUI:
    """Tkinter-GUI für den Sitzplan-Generator (reine View)."""

    def __init__(self, model: "Model", controller: "Controller"):
        self.root = tk.Tk()
        self.root.title("Sitzplan-Generator")
        self.root.geometry("1200x700")

        self.model = model
        self.controller = controller

        # Hauptlayout: Canvas (85%) + Controls (15%) + Statusleiste
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas-Klasse erstellen
        self.classroom_canvas = ClassroomCanvas(main_frame, model)

        # Control Panel (rechts, 15%)
        control_frame = tk.Frame(main_frame, bg="lightgray")
        control_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=10, pady=10)

        # Namensliste
        tk.Label(
            control_frame, text="Namen:", font=("Arial", 9, "bold"), bg="lightgray"
        ).pack(anchor=tk.W)
        self.student_listbox = tk.Listbox(control_frame, height=10, width=20)
        self.student_listbox.pack(fill=tk.BOTH, expand=True, pady=5)

        # Buttons
        button_frame = tk.Frame(control_frame, bg="lightgray")
        button_frame.pack(fill=tk.X, pady=5)

        tk.Button(
            button_frame,
            text="Generiere",
            command=self._on_generate_clicked,
            font=("Arial", 9),
        ).pack(fill=tk.X, pady=2)

        # Statusleiste am unteren Rand
        self.status_frame = tk.Frame(self.root, relief=tk.SUNKEN, bd=2)
        self.status_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Status-Label (oben)
        self.status_label = tk.Label(
            self.status_frame,
            text="Status",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=5,
        )
        self.status_label.pack(anchor=tk.W, fill=tk.X)

        # Fehler-Details (unten, scrollbar falls nötig)
        self.error_label = tk.Label(
            self.status_frame,
            text="",
            font=("Arial", 9),
            padx=10,
            pady=5,
            justify=tk.LEFT,
        )
        self.error_label.pack(anchor=tk.W, fill=tk.X)

        self._update_view()

    def run(self):
        """Startet die GUI Mainloop."""
        self.root.mainloop()

    def _on_generate_clicked(self):
        """Wird aufgerufen, wenn Generiere-Button geklickt wird."""
        self.controller.on_generate_requested()
        self._update_view()

    def _update_view(self):
        self.classroom_canvas.draw()
        self._update_student_listbox()
        self._update_status()

    def _update_student_listbox(self):
        self.student_listbox.delete(0, tk.END)
        for student in self.model.students:
            self.student_listbox.insert(tk.END, student.name)

    def _update_status(self):
        """Aktualisiert die Statusleiste mit Farbe und Constraint-Fehlern."""
        if self.model.is_valid():
            self.status_frame.config(bg="lightgreen")
            self.status_label.config(text="✓ GÜLTIG", bg="lightgreen", fg="darkgreen")
            self.error_label.config(text="", bg="lightgreen")
        else:
            self.status_frame.config(bg="lightcoral")
            self.status_label.config(text="✗ UNGÜLTIG", bg="lightcoral", fg="darkred")

            error_text = "Fehler:\n" + "\n".join(
                f"  • {name}" for name in self.model.get_failed_constraints()
            )
            self.error_label.config(text=error_text, bg="lightcoral")
