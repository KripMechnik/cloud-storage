FROM python:3.10

WORKDIR /app

RUN mkdir -p app/file

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/file

EXPOSE 8004

CMD ["uvicorn", "app.file.main:app", "--host", "0.0.0.0", "--port", "8004"]