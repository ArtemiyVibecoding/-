FROM python:3.12-slim

WORKDIR /app

# Зависимости (кэшируются отдельным слоем)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код бота
COPY . .

# Render передаёт PORT автоматически
EXPOSE 10000

CMD ["python", "bot.py"]
