FROM python:3.10

WORKDIR /app

RUN mkdir -p app/subscription

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/subscription

EXPOSE 8007

CMD ["uvicorn", "app.subscription.main:app", "--host", "0.0.0.0", "--port", "8007"]