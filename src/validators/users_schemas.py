import re


def validate_password_strength(password: str) -> None:
    if len(password) < 8:
        raise ValueError("Пароль должен содержать минимум 8 символов")

    if not re.search(r"[a-z]", password):
        raise ValueError("Пароль должен содержать хотя бы одну строчную букву")

    if not re.search(r"[A-Z]", password):
        raise ValueError("Пароль должен содержать хотя бы одну заглавную букву")

    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        raise ValueError("Пароль должен содержать хотя бы один специальный символ")
