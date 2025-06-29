from typing import TypeVar, Iterable, Callable


T = TypeVar('T')


def validate_all_ids_found(
        input_ids: list[int],
        founded_objects: Iterable[T],
        id_getter_function: Callable[[T], int],
        exception_builder: Callable[[T], Exception]
):
    if not founded_objects:
        raise exception_builder(input_ids)
    founded_ids = {id_getter_function(obj) for obj in founded_objects}
    missing_ids = list(set(input_ids) - founded_ids)
    if missing_ids:
        raise exception_builder(missing_ids)
