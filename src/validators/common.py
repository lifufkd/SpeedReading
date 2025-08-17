from typing import TypeVar, Callable, Iterable

from src.core.exceptions import UpdateRelationIdsInvalid

T = TypeVar('T')


def is_number_in_list(number: int, list_: list[int]) -> bool:
    if number in list_:
        return True

    return False


def is_number_not_in_list(number: int, list_: list[int]) -> bool:
    if number in list_:
        return False

    return True


def is_update_relation_ids_is_valid(
        relation_ids: list[int],
        add_relation_ids: list[int],
        delete_relation_ids: list[int]
) -> None:
    wrong_add_ids = list(set(relation_ids) & set(add_relation_ids))
    wrong_delete_ids = list(set(delete_relation_ids) - set(relation_ids))

    if wrong_add_ids:
        raise UpdateRelationIdsInvalid(wrong_add_ids=wrong_add_ids)
    if wrong_delete_ids:
        raise UpdateRelationIdsInvalid(wrong_delete_ids=wrong_delete_ids)


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
