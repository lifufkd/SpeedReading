def validate_at_least_one_filled(values: dict[str, any]) -> dict[str, any]:
    if all(v in (None, [], {}, '') for v in values.values()):
        raise ValueError("At least one field must be filled.")
    return values


def ensure_no_duplicates(value: list[int], field_name: str) -> list[int]:
    if len(value) != len(set(value)):
        raise ValueError(f"Field `{field_name}` contains duplicate values.")
    return value


def ensure_no_duplicates_across_fields(values: dict[str, list[int]]) -> dict[str, list[int]]:
    all_ids = []
    for v in values.values():
        all_ids.extend(v or [])
    if len(all_ids) != len(set(all_ids)):
        raise ValueError("Duplicate IDs are not allowed across fields.")
    return values
