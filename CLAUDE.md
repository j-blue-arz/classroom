CLAUDE NEVER USES EM DASHES. Instead, ALWAYS use commas or hyphens.

CLAUDE NEVER ATTRIBUTES HIMSELF in Git commits.

---

# Rules for Code Changes in This Project

## Files

There are exactly 5 Python files. NEVER create new .py files.
All additions go into one of the existing files:
- `classroom.py` - classroom data model
- `students.py` - student data model
- `constraints.py` - rules and algorithm
- `main.py` - Model, Controller, entry point
- `gui.py` - GUI (tkinter)

## Import Rules (strict)

```
classroom.py   <- no imports from this project
students.py    <- no imports from this project
constraints.py <- may only import classroom
gui.py         <- may only import classroom, students (TYPE_CHECKING only for main)
main.py        <- may import all
```

Violating these rules is forbidden, even if it seems more convenient.

## MVC Rules

- `ClassroomCanvas` has NO reference to Controller. User events go via callbacks.
- `SeatingPlanGUI` is the ONLY class that calls Controller methods.
- `Controller` has NO reference to GUI classes. Never calls `_update_view()`.
- GUI logic (colors, widgets, canvas) stays in `gui.py`.
- Business logic (assignments, validation) stays in `Model`/`Controller`.

## Where New Code Belongs

- New constraint rule: subclass `Constraint` in `constraints.py`, add to `active_constraints`
- New button: `_on_x_clicked` handler in `SeatingPlanGUI`, button widget in `__init__`
- New model logic: method on `Model` (e.g. `save`, `load`)
- New controller action: method on `Controller`, delegates to `Model`

## Code Style (grade 9, age 15)

- English names for classes, functions, variables. German comments and docstrings.
- Allowed: `list`, `dict`, `for` loops, `if`/`else`, functions with parameters and return values, `@dataclass`, simple inheritance (`class X(Y)`).
- NOT allowed: generators, `lambda`, decorators (except `@dataclass`, `@abstractmethod`, `@property`), complex comprehensions, `*args`/`**kwargs`, metaclasses, context managers (except `with open(...)`).
- External packages: NONE. Only Python stdlib (tkinter, json, random, abc, dataclasses).

## Scope of Changes

- Only change what is explicitly requested. No opportunistic refactoring.
- No new abstractions unless required by the task.
- Do not "improve" existing code that is not part of the task.
- Report errors rather than silently working around them.
