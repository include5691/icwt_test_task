FROM python:3

WORKDIR /app

ENV PYTHONUNBUFFERED=1

COPY task /app/task
COPY requirements.txt .env /app/

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "-m", "task.main"]