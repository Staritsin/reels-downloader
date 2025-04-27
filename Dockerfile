FROM python:3.11-slim

# Устанавливаем ffmpeg
RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта
COPY . .

# Открываем порт 8080
EXPOSE 8080

# Запускаем приложение
CMD ["python", "main.py"]
