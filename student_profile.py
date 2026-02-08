
from dataclasses import dataclass
from typing import List


@dataclass
class StudentProfile:

    name: str
    id: int
    grades: List[int]

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'id': self.id,
            'grades': self.grades
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'StudentProfile':
        return cls(
            name=data['name'],
            id=data['id'],
            grades=data['grades']
        )
