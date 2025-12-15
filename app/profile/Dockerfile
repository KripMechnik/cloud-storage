FROM python:3.10

WORKDIR /app

RUN mkdir -p app/profile

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/profile

EXPOSE 8006

CMD ["uvicorn", "app.profile.main:app", "--host", "0.0.0.0", "--port", "8006"]