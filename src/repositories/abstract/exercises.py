from abc import ABC, abstractmethod

from src.models.exercise import Exercises
from src.dto.exercises import CreateExerciseDTO


class ExerciseAbstract(ABC):

    @abstractmethod
    async def get_all(self) -> list[Exercises]:
        pass

    @abstractmethod
    async def add(self, data: CreateExerciseDTO) -> Exercises:
        pass

    @abstractmethod
    async def get_by_id(self, exercise_id: int) -> Exercises:
        pass

    @abstractmethod
    async def add(self, data: CreateExerciseDTO) -> Exercises:
        pass

    @abstractmethod
    async def delete(self, exercise_id: int) -> bool | None:
        pass
