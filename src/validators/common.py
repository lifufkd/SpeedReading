def is_number_in_list(number: int, list_: list[int]) -> bool:
    if number in list_:
        return True

    return False


def is_number_not_in_list(number: int, list_: list[int]) -> bool:
    if number in list_:
        return False

    return True
