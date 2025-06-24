from pydantic import BaseModel
from typing import Type, TypeVar, List

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)


async def dto_to_schema(
    dto_instance: T,
    schema_model: Type[U],
) -> U:
    return schema_model.model_validate(dto_instance.model_dump())


async def many_dto_to_schema(
    dto_instances: List[T],
    schema_model: Type[U],
) -> List[U]:
    return [await dto_to_schema(dto, schema_model) for dto in dto_instances]
