from typing import Callable, TypeVar, Awaitable, Any

from src.validators.common import is_update_relation_ids_is_valid, validate_all_ids_found


T = TypeVar("T")
R = TypeVar("R")


class LearningHelper:
    def __init__(self):
        pass

    async def update_relation(
            self,
            entity: T,
            add_ids: list[int],
            delete_ids: list[int],
            get_related: Callable[[T], list[R]],
            id_getter: Callable[[R], int],
            repo_get_by_ids: Callable[[list[int]], Awaitable[list[R]]],
            exception: type[Exception],
            uow: Any,
    ) -> Any:
        related = get_related(entity)
        existed_ids = [id_getter(item) for item in related]

        is_update_relation_ids_is_valid(
            relation_ids=existed_ids,
            add_relation_ids=add_ids,
            delete_relation_ids=delete_ids,
        )

        entities_to_update = await repo_get_by_ids(add_ids + delete_ids)
        validate_all_ids_found(
            input_ids=add_ids + delete_ids,
            founded_objects=entities_to_update,
            id_getter_function=id_getter,
            exception_builder=exception,
        )

        for related_entity in entities_to_update:
            related_id = id_getter(related_entity)
            if related_id in add_ids:
                related.append(related_entity)
            elif related_id in delete_ids:
                related.remove(related_entity)

        await uow.flush()
