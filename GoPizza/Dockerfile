# Вихідний образ
FROM python:3.11

# Робоча директорія в контейнері
WORKDIR /app

# Копіюємо залежності
COPY requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# Відкриваємо порт
EXPOSE 8000

# Запуск сервера за замовчуванням
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
