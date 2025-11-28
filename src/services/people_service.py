"""Person management workflows."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from src.core.models import Face, Person


def merge_people(source: Person, target: Person) -> Person:
    """Mark source as merged into target."""
    source.merged_into_id = target.id
    return target


def rename_person(person: Person, new_name: str) -> Person:
    person.display_name = new_name
    return person


@dataclass
class PersonSummary:
    person: Person
    faces: list[Face]


def get_person_summaries(persons: Iterable[Person]) -> list[PersonSummary]:
    return [PersonSummary(person=p, faces=[]) for p in persons]
