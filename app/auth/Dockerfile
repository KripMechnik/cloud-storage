FROM python:3.10

WORKDIR /app

RUN mkdir -p app/auth

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/auth

EXPOSE 8002

CMD ["uvicorn", "app.auth.main:app", "--host", "0.0.0.0", "--port", "8002"]