"""
Liste der Schülerinnen und Schüler.
"""

from dataclasses import dataclass


@dataclass
class Student:
    """Repräsentiert eine Schülerin oder einen Schüler."""

    name: str


student_list: list[Student] = [
    Student("Alice"),
    Student("Bob"),
    Student("Charlie"),
    Student("Diana"),
    Student("Enzo"),
    Student("Fiona"),
    Student("Gustav"),
    Student("Hannah"),
    Student("Ivano"),
    Student("Julia"),
    Student("Klaus"),
    Student("Luise"),
]
