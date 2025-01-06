# Указываем базовый образ с Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы бота и зависимости
COPY bot-weather.py requirements.txt ./

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запускаем контейнер без привилегий
USER 65534

# Указываем команду запуска
CMD ["python", "bot-weather.py"]
