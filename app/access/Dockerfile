FROM python:3.10

WORKDIR /app

RUN mkdir -p app/access

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/access

EXPOSE 8000

CMD ["uvicorn", "app.access.main:app", "--host", "0.0.0.0", "--port", "8000"]