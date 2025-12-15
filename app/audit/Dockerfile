FROM python:3.10

WORKDIR /app

RUN mkdir -p app/audit

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app/audit

EXPOSE 8001

CMD ["uvicorn", "app.audit.main:app", "--host", "0.0.0.0", "--port", "8001"]