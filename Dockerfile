FROM python:3.11-slim

# 3. Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# 4. Копируем файлы зависимостей
COPY requirements.txt .

# 5. Устанавливаем Python-зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# 6. Копируем остальной код приложения
COPY . .

# 7. Создаём пользователя и переключаемся на него
RUN useradd -m fastapi_user
USER fastapi_user

# Указываем точку входа
CMD ["./entrypoint.sh"]