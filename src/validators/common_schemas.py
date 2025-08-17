def validate_non_empty(instance):
    if not instance.add_ids and not instance.delete_ids:
        raise ValueError("Either 'add_ids' or 'delete_ids' must contain at least one ID.")
    return instance


def validate_no_duplicates(instance):
    if set(instance.add_ids) & set(instance.delete_ids):
        raise ValueError("Duplicate IDs between add_ids and delete_ids")
    return instance
