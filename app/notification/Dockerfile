FROM python:3.10

WORKDIR /app

RUN mkdir -p app/notification

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/notification

EXPOSE 8005

CMD ["uvicorn", "app.notification.main:app", "--host", "0.0.0.0", "--port", "8005"]