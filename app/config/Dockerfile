FROM python:3.10

WORKDIR /app

RUN mkdir -p app/config

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/config

EXPOSE 8003

CMD ["uvicorn", "app.config.main:app", "--host", "0.0.0.0", "--port", "8003"]